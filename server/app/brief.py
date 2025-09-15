from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/api")

@router.get("/brief")
def get_brief():
    today = datetime.utcnow()
    macro = {
        "stance": "neutru",
        "notes": [
            {"text": "Randamente reale stabile; volatilități moderate.", "citation": {"url": "#"}},
            {"text": "USD mixt; calendar macro ușor încărcat.", "citation": {"url": "#"}},
        ],
    }
    ideas = {
        "EQ_INV": [
            {"text": "Rebalansare spre quality [1]", "score": 0.62, "uncertainty": "med", "citations": [{"url": "#"}]},
            {"text": "Cost mediu în timp pentru defensiv [2]", "score": 0.55, "uncertainty": "med", "citations": [{"url": "#"}]},
            {"text": "ETF broad‑market la discount [3]", "score": 0.58, "uncertainty": "low", "citations": [{"url": "#"}]},
        ],
        "EQ_MOM": [
            {"text": "Momentum post‑earnings pe volum [1]", "score": 0.68, "uncertainty": "med", "citations": [{"url": "#"}]},
            {"text": "Gap & go cu invalidare clară [2]", "score": 0.60, "uncertainty": "med", "citations": [{"url": "#"}]},
            {"text": "Breakout sectorial sincronizat [3]", "score": 0.57, "uncertainty": "high", "citations": [{"url": "#"}]},
        ],
        "OPT_INCOME": [
            {"text": "Covered calls pe vol scăzută [1]", "score": 0.63, "uncertainty": "low", "citations": [{"url": "#"}]},
            {"text": "Puturi cash‑secured lângă suport [2]", "score": 0.59, "uncertainty": "med", "citations": [{"url": "#"}]},
            {"text": "Calendar spreads conservatoare [3]", "score": 0.56, "uncertainty": "med", "citations": [{"url": "#"}]},
        ],
    }
    calendar = [
        {"time": "08:00", "type": "macro", "title": f"Brief zilnic {today.strftime('%Y-%m-%d')}"},
        {"time": "14:30", "type": "earnings", "symbol": "AAPL", "title": "Raport trimestrial"},
        {"time": "18:00", "type": "macro", "title": "Minuta FOMC"},
    ]
    return {"macro": macro, "ideas": ideas, "calendar": calendar}
