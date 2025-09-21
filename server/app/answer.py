from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, math, time, logging, json, re
import httpx
from .db import get_conn
from .observability import record_query_event
from .config import settings

router = APIRouter(prefix="/api")

class AnswerRequest(BaseModel):
    question: str
    collection: str

class AnswerResponse(BaseModel):
    answer: dict
    citations: list

# Simple embed helper
_embed_client = None

def embed_text(text: str):
    """Return list[float] or None if not configured/available."""
    global _embed_client
    project = os.getenv("VERTEX_PROJECT_ID")
    location = os.getenv("VERTEX_LOCATION", "us-central1")
    model = os.getenv("EMBED_MODEL", "text-embedding-004")
    if not project:
        return None
    try:
        from vertexai import init
        try:
            # Prefer preview path for text-embedding-004 on newer SDKs
            from vertexai.preview.language_models import TextEmbeddingModel  # type: ignore
        except Exception:
            from vertexai.language_models import TextEmbeddingModel  # type: ignore
        init(project=project, location=location)
        mdl = TextEmbeddingModel.from_pretrained(model)
        emb = mdl.get_embeddings([text])[0]
        vals = getattr(emb, "values", None) or getattr(getattr(emb, "embedding", None), "values", None)
        return list(vals) if vals is not None else None
    except Exception:
        logging.getLogger("app.answer").exception("vertex_embed_error")
        return None

@router.post("/answer", response_model=AnswerResponse)
def post_answer(payload: AnswerRequest):
    t0 = time.perf_counter()
    q = (payload.question or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Empty question")

    # Try to embed and normalize (cosine)
    qvec = embed_text(q)
    if qvec is not None:
        nrm = math.sqrt(sum(v * v for v in qvec)) or 1.0
        qvec = [v / nrm for v in qvec]

    conn = get_conn()
    citations = []
    num_candidates = 0

    if qvec is not None:
        # Retrieve top-K by vector distance
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, doc_id, page, chunk_index, text, (embedding_vec <-> %s::vector) AS dist
                    FROM fragments
                    WHERE collection = %s AND embedding_vec IS NOT NULL
                    ORDER BY dist ASC
                    LIMIT %s
                    """,
                    (qvec, payload.collection, settings.retrieval_k)
                )
                rows = cur.fetchall()
        except Exception:
            logging.getLogger("app.answer").exception("answer_query_error")
            rows = []
        num_candidates = len(rows)
        tau = float(getattr(settings, "relevance_tau", 0.20))

        # Build candidates with similarity
        cands = []
        for r in rows:
            dist = float(r[5]) if r[5] is not None else 1.0
            sim = 1.0 - dist
            cands.append({
                "id": r[0],
                "doc_id": r[1],
                "page": r[2],
                "chunk_index": r[3],
                "text": r[4] or "",
                "sim": sim,
            })

        # Optional: rerank if configured
        reranked = cands
        if settings.rerank_url:
            t_r = time.perf_counter()
            try:
                # Cohere v2-compatible body; also keeps a generic structure
                rr_model = os.getenv("RERANK_MODEL", "rerank-english-v3.0")
                body = {
                    "query": q,
                    "candidates": [{"id": c["id"], "text": (c["text"] or "")[:2000]} for c in cands],
                    "documents": [{"id": c["id"], "text": (c["text"] or "")[:2000]} for c in cands],
                    "model": rr_model,
                    "top_n": max(1, int(getattr(settings, "retrieval_n", 5)))
                }
                headers = {"Content-Type": "application/json"}
                if settings.rerank_api_key:
                    headers["Authorization"] = f"Bearer {settings.rerank_api_key}"
                with httpx.Client(timeout=10.0) as client:
                    resp = client.post(str(settings.rerank_url), json=body, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                results = data.get("results") or data.get("scores") or []
                score_map = {}
                if isinstance(results, list) and results and isinstance(results[0], dict) and ("relevance_score" in results[0] or "document" in results[0]):
                    for it in results:
                        sc = float(it.get("relevance_score", it.get("score", 0.0)) or 0.0)
                        doc = it.get("document") or {}
                        sid = doc.get("id") or None
                        if sid is not None:
                            score_map[str(sid)] = sc
                        else:
                            idx = it.get("index")
                            if isinstance(idx, int) and 0 <= idx < len(reranked):
                                score_map[str(reranked[idx]["id"])] = sc
                elif isinstance(results, list) and results and not isinstance(results[0], dict) and len(results) == len(reranked):
                    for idx, sc in enumerate(results):
                        try:
                            score_map[str(reranked[idx]["id"])] = float(sc)
                        except Exception:
                            score_map[str(reranked[idx]["id"])] = 0.0
                if score_map:
                    for c in reranked:
                        c["rerank_score"] = float(score_map.get(str(c["id"]), 0.0))
                    reranked = sorted(reranked, key=lambda x: x.get("rerank_score", 0.0), reverse=True)
                else:
                    reranked = sorted(reranked, key=lambda x: x.get("sim", 0.0), reverse=True)
            except Exception:
                logging.getLogger("app.answer").exception("rerank_error")
                reranked = sorted(reranked, key=lambda x: x.get("sim", 0.0), reverse=True)
            finally:
                _ = int((time.perf_counter() - t_r) * 1000)
        else:
            reranked = sorted(reranked, key=lambda x: x.get("sim", 0.0), reverse=True)

        # Filter by tau and keep top-N
        kept = []
        for c in reranked:
            if float(c.get("sim", 0.0)) >= tau:
                kept.append(c)
            if len(kept) >= int(getattr(settings, "retrieval_n", 5)):
                break
        for c in kept:
            citations.append({
                "label": c["id"],
                "doc_id": c["doc_id"],
                "page": c["page"],
                "chunk_index": c["chunk_index"],
                "preview": (c["text"] or "")[:240],
                "url": "#"
            })
    else:
        # Fallback (no embeddings): simple latest docs in collection
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, doc_id, page, chunk_index, text
                FROM fragments
                WHERE collection = %s
                LIMIT %s
                """,
                (payload.collection, settings.retrieval_k)
            )
            rows = cur.fetchall()
        num_candidates = len(rows)
        for r in rows[: int(getattr(settings, "recovery_n", getattr(settings, "retrieval_n", 5)) )]:
            citations.append({
                "label": r[0],
                "doc_id": r[1],
                "page": r[2],
                "chunk_index": r[3],
                "preview": (r[4] or "")[:240],
                "url": "#"
            })

    # Require at least 3 citations for sufficient context
    insufficient = len(citations) < 3

    # If we have enough citations, try to build LLM answer context-only
    answer = {
        "thesis": "Răspuns de test bazat pe contexte găsite [n]",
        "setup": "Condiții sintetice pentru demo [n]",
        "invalidation": "Invalidare de demo [n]",
        "levels": "entry 100, stop 95, TP 112",
        "risk": "med",
        "uncertainty": "low"
    }

    if not insufficient and settings.llm_url:
        t_llm = time.perf_counter()
        try:
            # Build strict JSON-only prompt
            ctx_lines = []
            for idx, c in enumerate(citations, start=1):
                ctx_lines.append(f"[{idx}] doc={c.get('doc_id')} p.{c.get('page')} :: {c.get('preview')}")
            ctx = "\n".join(ctx_lines)
            sys_msg = (
                "You are a trading assistant. Answer strictly using ONLY the provided context snippets, "
                "citing with [n]. If context is insufficient, respond with an empty JSON fields. "
                "Return JSON object with keys: thesis, setup, invalidation, levels, risk, uncertainty."
            )
            user_msg = (
                f"Question: {q}\nContext:\n{ctx}\n"
            )
            payload_llm = {
                "model": settings.llm_model or "gpt-4o-mini",
                "temperature": float(getattr(settings, "llm_temperature", 0.2)),
                "messages": [
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": user_msg}
                ],
                "response_format": {"type": "json_object"}
            }
            headers = {"Content-Type": "application/json"}
            if settings.llm_api_key:
                headers["Authorization"] = f"Bearer {settings.llm_api_key}"
            with httpx.Client(timeout=15.0) as client:
                r = client.post(str(settings.llm_url), json=payload_llm, headers=headers)
            r.raise_for_status()
            data = r.json()
            # Try to extract JSON text from common schemas
            content_text = None
            if isinstance(data, dict):
                # OpenAI-like
                try:
                    content_text = data.get("choices", [{}])[0].get("message", {}).get("content")
                except Exception:
                    content_text = None
                # Generic fields
                if not content_text:
                    content_text = data.get("output_text") or data.get("text") or data.get("message")
                # Already structured
                if not content_text and isinstance(data.get("answer"), dict):
                    answer = data.get("answer")  # type: ignore
                elif isinstance(content_text, str):
                    # extract JSON
                    m = re.search(r"\{[\s\S]*\}$", content_text.strip())
                    raw_json = m.group(0) if m else content_text
                    try:
                        parsed = json.loads(raw_json)
                        if isinstance(parsed, dict):
                            answer = {
                                "thesis": str(parsed.get("thesis", "")),
                                "setup": str(parsed.get("setup", "")),
                                "invalidation": str(parsed.get("invalidation", "")),
                                "levels": str(parsed.get("levels", "")),
                                "risk": str(parsed.get("risk", "")),
                                "uncertainty": str(parsed.get("uncertainty", "")),
                            }
                    except Exception:
                        pass
        except Exception:
            logging.getLogger("app.answer").exception("llm_error")
        finally:
            llm_ms = int((time.perf_counter() - t_llm) * 1000)
            logging.getLogger("app.answer").info("llm_timing ms=%s", llm_ms)

    # Observability log
    try:
        logger = logging.getLogger("app.answer")
        duration_ms = int((time.perf_counter() - t0) * 1000)
        logger.info(
            "answer_timing collection=%s duration_ms=%s candidates=%s citations=%s k=%s n=%s tau=%s embedded=%s qlen=%s insufficient=%s",
            payload.collection,
            duration_ms,
            num_candidates,
            len(citations),
            getattr(settings, "retrieval_k", None),
            getattr(settings, "retrieval_n", None),
            getattr(settings, "relevance_tau", None),
            qvec is not None,
            len(q),
            insufficient,
        )
        try:
            record_query_event(duration_ms=duration_ms, candidates=num_candidates, citations=len(citations), insufficient=insufficient)
        except Exception:
            pass
    except Exception:
        pass

    if insufficient:
        return AnswerResponse(answer={"thesis":"","setup":"","invalidation":"","levels":"","risk":"—","uncertainty":"—"}, citations=[])

    return AnswerResponse(answer=answer, citations=citations)
