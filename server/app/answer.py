from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from .db import get_conn

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
    model = os.getenv("EMBED_MODEL", "textembedding-gecko@003")
    if not project:
        return None
    try:
        from google.cloud import aiplatform  # lazy import
        if _embed_client is None:
            aiplatform.init(project=project, location=location)
        emb = aiplatform.TextEmbeddingModel.from_pretrained(model).get_embeddings([text])
        vals = getattr(emb[0], 'values', None)
        if vals is None and hasattr(emb[0], 'embedding'):
            vals = getattr(emb[0].embedding, 'values', None)
        return list(vals) if vals is not None else None
    except Exception:
        return None

@router.post("/answer", response_model=AnswerResponse)
def post_answer(payload: AnswerRequest):
    q = (payload.question or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Empty question")
    # Try to embed (optional in MVP)
    _qvec = embed_text(q)

    # MVP retrieval: simple fetch by collection (will replace with vector search)
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, doc_id, page, chunk_index, text
            FROM fragments
            WHERE collection = %s
            LIMIT 8
            """,
            (payload.collection,)
        )
        rows = cur.fetchall()

    if not rows:
        return AnswerResponse(answer={"thesis":"","setup":"","invalidation":"","levels":"","risk":"—","uncertainty":"—"}, citations=[])

    top = rows[:5]
    citations = []
    for r in top:
        citations.append({
            "label": r[0],
            "doc_id": r[1],
            "page": r[2],
            "chunk_index": r[3],
            "preview": (r[4] or "")[:240],
            "url": "#"
        })

    if len(citations) < 3:
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
