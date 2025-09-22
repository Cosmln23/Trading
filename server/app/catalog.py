from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any
from .db import get_conn

router = APIRouter(prefix="/api")


def _infer_kind(file_name: Optional[str]) -> str:
    name = (file_name or "").lower()
    hints_news = ("news", "stire", "stiri", "daily", "nyt_", "wsj_", "bloomberg_", "reuters_")
    for h in hints_news:
        if h in name:
            return "news"
    return "book"


@router.get("/catalog")
def get_catalog(collection: Optional[str] = Query(default=None), q: Optional[str] = Query(default=None), limit: int = Query(default=200, ge=1, le=1000)):
    conn = get_conn()
    items: List[Dict[str, Any]] = []
    with conn.cursor() as cur:
        # Aggregate uploads as documents; join with fragments count
        cur.execute(
            """
            WITH uh AS (
                SELECT doc_id,
                       max(file_name) AS file_name,
                       max(collection) AS collection,
                       max(created_at) AS created_at,
                       sum(inserted_count) AS inserted_sum,
                       sum(embedded_count) AS embedded_sum,
                       bool_or(coalesce(ocr_used,false)) AS ocr_used,
                       max(kind) AS kind
                FROM upload_history
                GROUP BY doc_id
            ), fr AS (
                SELECT doc_id, count(*) AS fragments
                FROM fragments
                GROUP BY doc_id
            )
            SELECT uh.doc_id, uh.file_name, uh.collection, uh.created_at, uh.inserted_sum, uh.embedded_sum, uh.ocr_used, coalesce(fr.fragments,0) AS fragments, uh.kind
            FROM uh
            LEFT JOIN fr ON fr.doc_id = uh.doc_id
            ORDER BY uh.created_at DESC NULLS LAST
            """
        )
        rows = cur.fetchall()
        for r in rows:
            rec = {
                "doc_id": r[0],
                "file_name": r[1],
                "collection": r[2],
                "created_at": (r[3].isoformat() if r[3] else None),
                "inserted": int(r[4] or 0),
                "embedded": int(r[5] or 0),
                "ocr_used": bool(r[6]) if r[6] is not None else False,
                "fragments": int(r[7] or 0),
                "kind": r[8] or None,
            }
            items.append(rec)

    # Filters
    if collection:
        items = [x for x in items if (x.get("collection") == collection)]
    if q:
        qq = q.lower()
        items = [x for x in items if qq in (x.get("file_name") or "").lower() or qq in (x.get("doc_id") or "").lower()]

    # Split by kind
    books: List[Dict[str, Any]] = []
    news: List[Dict[str, Any]] = []
    for x in items[:limit]:
        kind = (x.get("kind") or _infer_kind(x.get("file_name")))
        (news if kind == "news" else books).append(x)

    return JSONResponse(content={"books": books, "news": news, "count": {"books": len(books), "news": len(news)}})


@router.get("/upload_history")
def get_upload_history(limit: int = Query(default=50, ge=1, le=500)):
    items: List[Dict[str, Any]] = []
    with get_conn().cursor() as cur:
        cur.execute(
            """
            SELECT id, file_name, file_size, file_hash, doc_id, collection, text_chars, chunk_count,
                   inserted_count, skipped_conflict_count, embedded_count, ocr_used, created_at
            FROM upload_history
            ORDER BY id DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cur.fetchall()
    for r in rows:
        items.append({
            "id": r[0],
            "file_name": r[1],
            "file_size": r[2],
            "file_hash": r[3],
            "doc_id": r[4],
            "collection": r[5],
            "text_chars": r[6],
            "chunk_count": r[7],
            "inserted_count": r[8],
            "skipped_conflict_count": r[9],
            "embedded_count": r[10],
            "ocr_used": bool(r[11]) if r[11] is not None else False,
            "created_at": (r[12].isoformat() if r[12] else None),
        })
    return JSONResponse(content={"list": items})


