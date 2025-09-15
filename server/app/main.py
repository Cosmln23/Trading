from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from pathlib import Path
import os
import psycopg

from .config import settings

app = FastAPI(title="Trading Assistant API", version="1.0.0")

# Same-origin: no CORS needed if UI+API same host. Keep CORS disabled by default.

@app.get("/health")
async def health():
    checks = {"vertex": "unknown", "db": "unknown", "reranker": "unknown", "llm": "unknown"}
    # DB check (non-blocking if DATABASE_URL missing)
    if settings.database_url:
        try:
            with psycopg.connect(settings.database_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
            checks["db"] = "ok"
        except Exception:
            checks["db"] = "fail"
    else:
        checks["db"] = "unset"
    # Others left as 'unknown' until implemented
    return {"status": "ok", "checks": checks}

@app.get("/api/settings")
async def get_settings():
    data = {
        "K": settings.retrieval_k,
        "N": settings.retrieval_n,
        "tau": settings.relevance_tau,
        "reranker": bool(settings.rerank_url),
        "mmr": True,
        "recency_boost": settings.recency_boost,
        "policy": "context-only" if settings.context_only else "unrestricted",
    }
    return JSONResponse(content=data)

# Optional: serve UI statically from repo root (../) for same-origin dev
repo_root = Path(__file__).resolve().parents[2]
ui_index = repo_root / "index.html"
if ui_index.exists():
    app.mount("/", StaticFiles(directory=str(repo_root), html=True), name="ui")
