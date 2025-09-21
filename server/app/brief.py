from fastapi import APIRouter
from datetime import datetime
from .db import get_conn

router = APIRouter(prefix="/api")

@router.get("/brief")
def get_brief():
    today = datetime.utcnow()
    macro = {
        "stance": "neutru",
        "notes": [],
    }

    # Try to attach a couple of real citations from latest fragments in EQ_INV
    try:
        with get_conn().cursor() as cur:
            cur.execute(
                """
                SELECT doc_id, left(text, 200)
                FROM fragments
                WHERE collection = %s
                ORDER BY created_at DESC
                LIMIT 2
                """,
                ("EQ_INV",),
            )
            rows = cur.fetchall()
        for _doc, _prev in rows:
            macro.setdefault("notes", []).append({
                "text": (_prev or "").replace("\n", " "),
                "citation": {"url": "#", "doc_id": _doc}
            })
    except Exception:
        # fallback static notes
        macro.setdefault("notes", []).extend([
            {"text": "Randamente reale stabile; volatilități moderate.", "citation": {"url": "#"}},
            {"text": "USD mixt; calendar macro ușor încărcat.", "citation": {"url": "#"}},
        ])
    ideas = {"EQ_INV": [], "EQ_MOM": [], "OPT_INCOME": []}

    def latest_citation_for(collection: str):
        try:
            with get_conn().cursor() as cur:
                cur.execute(
                    """
                    SELECT doc_id, left(text, 200)
                    FROM fragments
                    WHERE collection = %s
                    ORDER BY created_at DESC
                    LIMIT 1
                    """,
                    (collection,),
                )
                r = cur.fetchone()
            if r:
                return {"url": "#", "doc_id": r[0], "preview": (r[1] or "").replace("\n", " ")}
        except Exception:
            pass
        return {"url": "#"}

    ideas["EQ_INV"] = [
        {"text": "Rebalansare spre quality [1]", "score": 0.62, "uncertainty": "med", "citations": [latest_citation_for("EQ_INV")]},
        {"text": "Cost mediu în timp pentru defensiv [2]", "score": 0.55, "uncertainty": "med", "citations": [latest_citation_for("EQ_INV")]},
        {"text": "ETF broad‑market la discount [3]", "score": 0.58, "uncertainty": "low", "citations": [latest_citation_for("EQ_INV")]},
    ]
    ideas["EQ_MOM"] = [
        {"text": "Momentum post‑earnings pe volum [1]", "score": 0.68, "uncertainty": "med", "citations": [latest_citation_for("EQ_MOM_PEAD")]},
        {"text": "Gap & go cu invalidare clară [2]", "score": 0.60, "uncertainty": "med", "citations": [latest_citation_for("EQ_MOM_PEAD")]},
        {"text": "Breakout sectorial sincronizat [3]", "score": 0.57, "uncertainty": "high", "citations": [latest_citation_for("EQ_MOM_PEAD")]},
    ]
    ideas["OPT_INCOME"] = [
        {"text": "Covered calls pe vol scăzută [1]", "score": 0.63, "uncertainty": "low", "citations": [latest_citation_for("OPT_INCOME")]},
        {"text": "Puturi cash‑secured lângă suport [2]", "score": 0.59, "uncertainty": "med", "citations": [latest_citation_for("OPT_INCOME")]},
        {"text": "Calendar spreads conservatoare [3]", "score": 0.56, "uncertainty": "med", "citations": [latest_citation_for("OPT_INCOME")]},
    ]
    calendar = [
        {"time": "08:00", "type": "macro", "title": f"Brief zilnic {today.strftime('%Y-%m-%d')}"},
        {"time": "14:30", "type": "earnings", "symbol": "AAPL", "title": "Raport trimestrial"},
        {"time": "18:00", "type": "macro", "title": "Minuta FOMC"},
    ]
    return {"macro": macro, "ideas": ideas, "calendar": calendar}
