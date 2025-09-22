from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from .db import get_conn

router = APIRouter(prefix="/api")


class Holding(BaseModel):
    symbol: str
    quantity: Optional[float] = None
    cost: Optional[float] = None
    tags: Optional[str] = None


class PortfolioSnapshotIn(BaseModel):
    ts: Optional[str] = None
    note: Optional[str] = None
    source: Optional[str] = None
    holdings: List[Holding]


@router.post('/portfolio')
def post_portfolio(payload: PortfolioSnapshotIn):
    if not payload.holdings:
        raise HTTPException(status_code=400, detail='holdings required')
    with get_conn().cursor() as cur:
        cur.execute("INSERT INTO portfolio_snapshots (ts, note, source) VALUES (COALESCE(%s, now()), %s, %s) RETURNING id", (payload.ts, payload.note, payload.source))
        sid = cur.fetchone()[0]
        for h in payload.holdings:
            cur.execute(
                "INSERT INTO portfolio_holdings (snapshot_id, symbol, quantity, cost, tags) VALUES (%s,%s,%s,%s,%s)",
                (sid, h.symbol.upper(), h.quantity, h.cost, h.tags)
            )
        get_conn().commit()
    return { 'ok': True, 'snapshot_id': sid }


@router.get('/portfolio/latest')
def get_portfolio_latest():
    with get_conn().cursor() as cur:
        cur.execute("SELECT id, ts, note, source FROM portfolio_snapshots ORDER BY ts DESC LIMIT 1")
        row = cur.fetchone()
        if not row:
            return { 'snapshot': None, 'holdings': [] }
        sid, ts, note, src = row
        cur.execute("SELECT symbol, quantity, cost, tags FROM portfolio_holdings WHERE snapshot_id=%s ORDER BY symbol", (sid,))
        holds = cur.fetchall()
    return {
        'snapshot': { 'id': sid, 'ts': (ts.isoformat() if ts else None), 'note': note, 'source': src },
        'holdings': [ { 'symbol': r[0], 'quantity': float(r[1]) if r[1] is not None else None, 'cost': float(r[2]) if r[2] is not None else None, 'tags': r[3] } for r in holds ]
    }


