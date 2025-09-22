from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import time, uuid, datetime as dt
from .db import get_conn
from .answer import embed_text
from .config import settings
import math

router = APIRouter(prefix="/api")


class ChatCreateResponse(BaseModel):
    chat_id: str
    expires_at: Optional[str]


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatPostRequest(BaseModel):
    chat_id: Optional[str]
    collection: str
    message: str


class ChatPostResponse(BaseModel):
    chat_id: str
    messages: List[ChatMessage]


TTL_SECONDS = 24 * 3600


def _ensure_session(chat_id: Optional[str]) -> str:
    now = int(time.time())
    expires_at = dt.datetime.utcfromtimestamp(now + TTL_SECONDS)
    with get_conn().cursor() as cur:
        if chat_id:
            cur.execute("SELECT id FROM chat_sessions WHERE id=%s AND (expires_at IS NULL OR expires_at > now())", (chat_id,))
            row = cur.fetchone()
            if row:
                return chat_id
        sid = uuid.uuid4().hex[:32]
        cur.execute("INSERT INTO chat_sessions (id, expires_at) VALUES (%s,%s)", (sid, expires_at))
        get_conn().commit()
        return sid


def _portfolio_summary() -> str:
    with get_conn().cursor() as cur:
        cur.execute("SELECT id, ts FROM portfolio_snapshots ORDER BY ts DESC LIMIT 1")
        row = cur.fetchone()
        if not row:
            return ''
        sid = row[0]
        cur.execute("SELECT symbol, quantity, cost FROM portfolio_holdings WHERE snapshot_id=%s ORDER BY symbol LIMIT 50", (sid,))
        holds = cur.fetchall()
    parts = []
    for (sym, qty, cost) in holds:
        q = (float(qty) if qty is not None else 0)
        c = (float(cost) if cost is not None else 0)
        parts.append(f"{sym}:{q}@{c}")
    return "; ".join(parts)


@router.post('/chat/create', response_model=ChatCreateResponse)
def create_chat():
    sid = _ensure_session(None)
    with get_conn().cursor() as cur:
        cur.execute("SELECT expires_at FROM chat_sessions WHERE id=%s", (sid,))
        row = cur.fetchone()
    return ChatCreateResponse(chat_id=sid, expires_at=(row[0].isoformat() if row and row[0] else None))


@router.get('/chat/{chat_id}', response_model=ChatPostResponse)
def get_chat(chat_id: str):
    with get_conn().cursor() as cur:
        cur.execute("SELECT id FROM chat_sessions WHERE id=%s", (chat_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail='chat not found')
        cur.execute("SELECT role, content FROM chat_messages WHERE chat_id=%s ORDER BY ts ASC LIMIT 200", (chat_id,))
        rows = cur.fetchall()
    messages = [ChatMessage(role=r[0], content=r[1]) for r in rows]
    return ChatPostResponse(chat_id=chat_id, messages=messages)


@router.post('/chat', response_model=ChatPostResponse)
def post_chat(payload: ChatPostRequest):
    q = (payload.message or '').strip()
    if not q:
        raise HTTPException(status_code=400, detail='empty message')
    sid = _ensure_session(payload.chat_id)
    # store user message
    with get_conn().cursor() as cur:
        cur.execute("INSERT INTO chat_messages (chat_id, role, content) VALUES (%s,%s,%s)", (sid, 'user', q))
        get_conn().commit()
    # Retrieval: embed query and fetch top-K
    citations = []
    num_candidates = 0
    qvec = embed_text(q)
    if qvec is not None:
        nrm = math.sqrt(sum(v*v for v in qvec)) or 1.0
        qvec = [v/nrm for v in qvec]
        with get_conn().cursor() as cur:
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
        tau = float(getattr(settings, 'relevance_tau', 0.20))
        kept = []
        for r in rows:
            dist = float(r[5]) if r[5] is not None else 1.0
            sim = 1.0 - dist
            if sim >= tau:
                kept.append({ 'id': r[0], 'doc_id': r[1], 'text': (r[4] or '')[:1200] })
            if len(kept) >= int(getattr(settings, 'retrieval_n', 5)):
                break
        citations = kept

    # Portfolio summary
    port = _portfolio_summary()

    # Compose context-only answer (LLM optional; fallback template)
    answer_text = ''
    if settings.llm_url and settings.llm_api_key and citations:
        import httpx
        sys_prompt = 'Răspunde concis în română strict din fragmentele date; nu inventa. Explică de ce în 1-2 fraze. Ține cont de portofoliu (expuneri).'
        content = '\n\n'.join([f"[{i+1}] {c['text']}" for i,c in enumerate(citations)])
        user = f"Întrebare: {q}\nPortofoliu: {port or '—'}\nFragmente:\n{content}"
        body = { 'model': settings.llm_model or 'gpt-4o-mini', 'temperature': float(settings.llm_temperature or 0.2), 'messages': [ { 'role': 'system', 'content': sys_prompt }, { 'role': 'user', 'content': user } ] }
        headers = { 'Authorization': f"Bearer {settings.llm_api_key}", 'Content-Type': 'application/json' }
        try:
            with httpx.Client(timeout=15.0) as client:
                resp = client.post(str(settings.llm_url), json=body, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            answer_text = (data.get('choices') or [{}])[0].get('message',{}).get('content','').strip()
        except Exception:
            answer_text = f"(demo) Răspuns context-only pentru: {q} | portofoliu: {('n/a' if not port else 'ok')}"
    else:
        if citations:
            nums = ' '.join([f"[{i+1}]" for i,_ in enumerate(citations)])
            answer_text = f"Răspuns scurt bazat pe {len(citations)} fragmente {nums}. Întrebare: {q}. Portofoliu: {port or '—'}"
        else:
            answer_text = "Nu am găsit context suficient (încarcă surse sau relaxează filtrele)."

    with get_conn().cursor() as cur:
        cur.execute("INSERT INTO chat_messages (chat_id, role, content, citations) VALUES (%s,%s,%s,%s)", (sid, 'assistant', answer_text, len(citations)))
        get_conn().commit()
    with get_conn().cursor() as cur:
        cur.execute("SELECT role, content FROM chat_messages WHERE chat_id=%s ORDER BY ts ASC LIMIT 200", (sid,))
        rows = cur.fetchall()
    messages = [ChatMessage(role=r[0], content=r[1]) for r in rows]
    return ChatPostResponse(chat_id=sid, messages=messages)
