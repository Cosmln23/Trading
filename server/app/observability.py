from fastapi import APIRouter, Query
from typing import List, Dict, Any
from collections import deque
import time
import math

from .db import get_conn

router = APIRouter(prefix="/observability")

# In-memory ring buffer for lightweight observability (per instance)
_events: deque = deque(maxlen=1000)


def record_query_event(duration_ms: int, candidates: int, citations: int, insufficient: bool) -> None:
    _events.append({
        "ts": time.time(),
        "component": "query",
        "duration_ms": int(duration_ms),
        "candidates": int(candidates),
        "citations": int(citations),
        "insufficient": bool(insufficient),
    })


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


def _compute_kpis(window_sec: int) -> Dict[str, Any]:
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
                idxdef = row[1] or ""
                # Try to extract lists parameter
                lists_val = None
                # patterns: WITH (lists=256) or WITH (lists='256')
                import re
                m = re.search(r"lists\s*=\s*'?([0-9]+)'?", idxdef)
                if m:
                    lists_val = int(m.group(1))
                index["lists"] = lists_val
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
    return _compute_kpis(window)


@router.get("/events")
def get_events(limit: int = Query(200, ge=1, le=500)):
    out: List[Dict[str, Any]] = list(_events)
    out = out[-limit:]
    return {"list": out[::-1]}


