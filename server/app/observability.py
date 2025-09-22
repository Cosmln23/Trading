from fastapi import APIRouter, Query, Body
from typing import List, Dict, Any
from collections import deque
import time
import math
from .db import get_conn

router = APIRouter(prefix="/observability")

# In-memory ring buffer for lightweight observability (per instance)
_events: deque = deque(maxlen=1000)


def record_query_event(duration_ms: int, candidates: int, citations: int, insufficient: bool) -> None:
    ev = {
        "ts": time.time(),
        "component": "query",
        "duration_ms": int(duration_ms),
        "candidates": int(candidates),
        "citations": int(citations),
        "insufficient": bool(insufficient),
    }
    _events.append(ev)
    # Persist best-effort into DB
    try:
        with get_conn().cursor() as cur:
            cur.execute(
                "INSERT INTO events (ts, component, duration_ms, candidates, citations, insufficient, payload) VALUES (now(), %s, %s, %s, %s, %s, %s)",
                ("query", duration_ms, candidates, citations, insufficient, None),
            )
            get_conn().commit()
    except Exception:
        pass


def _percentile(sorted_values: List[float], p: float) -> float:
    if not sorted_values:
        return float("nan")
    if p <= 0:
        return float(sorted_values[0])
    if p >= 100:
        return float(sorted_values[-1])
    k = (len(sorted_values) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(sorted_values[int(k)])
    d0 = sorted_values[f] * (c - k)
    d1 = sorted_values[c] * (k - f)
    return float(d0 + d1)


def _compute_kpis_from_db(window_sec: int) -> Dict[str, Any]:
    try:
        with get_conn().cursor() as cur:
            cur.execute(
                """
                SELECT EXTRACT(EPOCH FROM ts), duration_ms, insufficient
                FROM events
                WHERE component='query' AND ts >= now() - (%s || ' seconds')::interval
                ORDER BY ts ASC
                """,
                (str(window_sec),),
            )
            rows = cur.fetchall()
        durations = [float(r[1]) for r in rows if r[1] is not None]
        insuff = [bool(r[2]) for r in rows]
        count = len(durations)
        if count == 0:
            return {"count": 0}
        p50 = _percentile(sorted(durations), 50.0)
        p95 = _percentile(sorted(durations), 95.0)
        rpm = count / (window_sec / 60.0)
        err = (sum(1 for x in insuff if x) / count) * 100.0
        # Index status
        index = {"present": False, "name": None, "lists": None}
        with get_conn().cursor() as cur:
            cur.execute(
                """
                SELECT indexname, indexdef
                FROM pg_indexes
                WHERE tablename='fragments' AND indexname='idx_fragments_vec'
                """
            )
            row = cur.fetchone()
            if row:
                index["present"] = True
                index["name"] = row[0]
                import re
                m = re.search(r"lists\s*=\s*'?([0-9]+)'?", row[1] or "")
                if m:
                    index["lists"] = int(m.group(1))
        return {
            "window_sec": window_sec,
            "rpm": round(rpm, 2),
            "error_rate_pct": round(err, 2),
            "p50_ms": int(p50),
            "p95_ms": int(p95),
            "count": count,
            "index": index,
        }
    except Exception:
        return {"count": 0}


def _compute_kpis_from_memory(window_sec: int) -> Dict[str, Any]:
    now = time.time()
    cutoff = now - max(60, window_sec)
    recent = [e for e in list(_events) if e.get("ts", 0) >= cutoff and e.get("component") == "query"]
    durations = sorted([float(e.get("duration_ms", 0.0)) for e in recent])
    count = len(recent)
    rpm = (count / (window_sec / 60.0)) if window_sec > 0 else 0.0
    err_rate = 0.0
    if count:
        err_rate = sum(1 for e in recent if e.get("insufficient")) / count * 100.0
    p50 = _percentile(durations, 50.0) if durations else float("nan")
    p95 = _percentile(durations, 95.0) if durations else float("nan")
    # Index status from Postgres
    index = {"present": False, "name": None, "lists": None}
    try:
        with get_conn().cursor() as cur:
            cur.execute(
                """
                SELECT indexname, indexdef
                FROM pg_indexes
                WHERE tablename='fragments' AND indexname='idx_fragments_vec'
                """
            )
            row = cur.fetchone()
            if row:
                index["present"] = True
                index["name"] = row[0]
                import re
                m = re.search(r"lists\s*=\s*'?([0-9]+)'?", row[1] or "")
                if m:
                    index["lists"] = int(m.group(1))
    except Exception:
        pass
    return {
        "window_sec": window_sec,
        "rpm": round(rpm, 2),
        "error_rate_pct": round(err_rate, 2),
        "p50_ms": None if math.isnan(p50) else int(p50),
        "p95_ms": None if math.isnan(p95) else int(p95),
        "count": count,
        "index": index,
    }


@router.get("/kpis")
def get_kpis(window: int = Query(300, ge=60, le=3600)):
    db = _compute_kpis_from_db(window)
    # Try to enrich with QA metrics if available
    try:
        with get_conn().cursor() as cur:
            cur.execute(
                """
                SELECT avg(precision5), avg(CASE WHEN hallucination THEN 1 ELSE 0 END)*100.0
                FROM qa_runs
                WHERE ts >= now() - (%s || ' seconds')::interval
                """,
                (str(window),),
            )
            row = cur.fetchone() or [None, None]
        if row[0] is not None:
            db["precision_at_5"] = float(row[0])
        if row[1] is not None:
            db["hallucination_rate_pct"] = float(row[1])
    except Exception:
        pass
    if db.get("count", 0) > 0:
        return db
    return _compute_kpis_from_memory(window)


@router.get("/events")
def get_events(limit: int = Query(200, ge=1, le=500)):
    out: List[Dict[str, Any]] = []
    # Try DB first
    try:
        with get_conn().cursor() as cur:
            cur.execute(
                "SELECT EXTRACT(EPOCH FROM ts), component, duration_ms, candidates, citations, insufficient FROM events ORDER BY ts DESC LIMIT %s",
                (limit,),
            )
            rows = cur.fetchall()
        for r in rows:
            out.append({
                "ts": float(r[0]),
                "component": r[1],
                "duration_ms": r[2],
                "candidates": r[3],
                "citations": r[4],
                "insufficient": r[5],
            })
    except Exception:
        pass
    if not out:
        out = list(_events)[-limit:][::-1]
    return {"list": out}


@router.get("/qa/questions")
def list_qa_questions(limit: int = Query(50, ge=1, le=200)):
    rows: List[Dict[str, Any]] = []
    try:
        with get_conn().cursor() as cur:
            cur.execute(
                "SELECT id, collection, question, expected_doc_ids FROM qa_questions ORDER BY id DESC LIMIT %s",
                (limit,),
            )
            for r in cur.fetchall():
                rows.append({
                    "id": r[0],
                    "collection": r[1],
                    "question": r[2],
                    "expected_doc_ids": list(r[3] or []),
                })
    except Exception:
        rows = []
    return {"list": rows}


@router.post("/qa/run")
def write_qa_run(
    question_id: int = Body(..., embed=True),
    citations_doc_ids: List[str] = Body(default=[], embed=True),
):
    # Fetch expected for question_id
    expected: List[str] = []
    try:
        with get_conn().cursor() as cur:
            cur.execute("SELECT expected_doc_ids FROM qa_questions WHERE id=%s", (question_id,))
            row = cur.fetchone()
            if row and row[0]:
                expected = list(row[0])
    except Exception:
        expected = []
    # Compute precision@5 and hallucination
    k = 5
    topk = citations_doc_ids[:k]
    inter = len([d for d in topk if d in set(expected)])
    precision5 = (inter / float(k)) if k else 0.0
    halluc = any((d not in set(expected)) for d in topk) if topk else True
    # Insert run
    try:
        with get_conn().cursor() as cur:
            cur.execute(
                "INSERT INTO qa_runs (question_id, citations_doc_ids, precision5, hallucination) VALUES (%s,%s,%s,%s)",
                (question_id, topk, precision5, halluc),
            )
            get_conn().commit()
    except Exception:
        pass
    return {"ok": True, "precision_at_5": precision5, "hallucination": halluc}


