from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import psycopg
from .db import get_conn

router = APIRouter(prefix="/api")

class JournalEntry(BaseModel):
    timestamp: str
    strategy: str
    symbol: str | None = None
    direction: str | None = None
    entry: float | None = None
    size: float | None = None
    stop: float | None = None
    tp: float | None = None
    rationale: str | None = None
    tags: str | None = None
    status: str | None = None
    rr: float | None = None
    pnl: float | None = None
    answer_id: str | None = None

@router.get("/journal")
def list_journal():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, timestamp, strategy, symbol, direction, entry, size, stop, tp, rationale, tags, status, rr, pnl, answer_id, created_at
            FROM journal ORDER BY id DESC LIMIT 200
            """
        )
        rows = cur.fetchall()
    result = []
    for r in rows:
        result.append({
            "id": r[0], "timestamp": r[1], "strategy": r[2], "symbol": r[3], "direction": r[4],
            "entry": r[5], "size": r[6], "stop": r[7], "tp": r[8], "rationale": r[9], "tags": r[10],
            "status": r[11], "rr": r[12], "pnl": r[13], "answer_id": r[14], "created_at": str(r[15])
        })
    return result

@router.post("/journal")
def add_journal(item: JournalEntry):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO journal (timestamp, strategy, symbol, direction, entry, size, stop, tp, rationale, tags, status, rr, pnl, answer_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING id
            """,
            (
                item.timestamp, item.strategy, item.symbol, item.direction,
                item.entry, item.size, item.stop, item.tp,
                item.rationale, item.tags, item.status, item.rr, item.pnl, item.answer_id
            )
        )
        new_id = cur.fetchone()[0]
        conn.commit()
    return {"id": new_id, "ok": True}
