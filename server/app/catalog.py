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
                       bool_or(coalesce(ocr_used,false)) AS ocr_used
                FROM upload_history
                GROUP BY doc_id
            ), fr AS (
                SELECT doc_id, count(*) AS fragments
                FROM fragments
                GROUP BY doc_id
            )
            SELECT uh.doc_id, uh.file_name, uh.collection, uh.created_at, uh.inserted_sum, uh.embedded_sum, uh.ocr_used, coalesce(fr.fragments,0) AS fragments
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
        kind = _infer_kind(x.get("file_name"))
        (news if kind == "news" else books).append(x)

    return JSONResponse(content={"books": books, "news": news, "count": {"books": len(books), "news": len(news)}})


