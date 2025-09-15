from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, math, time, logging
from .db import get_conn
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
        from vertexai.language_models import TextEmbeddingModel
        init(project=project, location=location)
        mdl = TextEmbeddingModel.from_pretrained(model)
        emb = mdl.get_embeddings([text])[0]
        vals = getattr(emb, "values", None) or getattr(getattr(emb, "embedding", None), "values", None)
        return list(vals) if vals is not None else None
    except Exception:
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
        # Vector search with cosine distance (<->); param cast to vector to avoid array operator error
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
        num_candidates = len(rows)
        # Apply tau and pick top N
        tau = float(getattr(settings, "relevance_tau", 0.20))
        for r in rows:
            dist = float(r[5]) if r[5] is not None else 1.0
            sim = 1.0 - dist
            if sim >= tau:
                citations.append({
                    "label": r[0],
                    "doc_id": r[1],
                    "page": r[2],
                    "chunk_index": r[3],
                    "preview": (r[4] or "")[:240],
                    "url": "#"
                })
        citations = citations[: int(getattr(settings, "retrieval_n", 5))]
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

    insufficient = len(citations) < 3
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
    except Exception:
        pass

    if insufficient:
        return AnswerResponse(answer={"thesis":"","setup":"","invalidation":"","levels":"","risk":"—","uncertainty":"—"}, citations=[])

    answer = {
        "thesis": "Răspuns de test bazat pe contexte găsite [n]",
        "setup": "Condiții sintetice pentru demo [n]",
        "invalidation": "Invalidare de demo [n]",
        "levels": "entry 100, stop 95, TP 112",
        "risk": "med",
        "uncertainty": "low"
    }
    return AnswerResponse(answer=answer, citations=citations)
