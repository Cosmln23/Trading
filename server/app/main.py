from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import Response, FileResponse
from pathlib import Path
import os
import logging
import base64
import psycopg

from .config import settings
from .answer import router as answer_router
from .brief import router as brief_router
from .upload import router as upload_router
from .journal import router as journal_router
from .db import get_conn

app = FastAPI(title="Trading Assistant API", version="1.0.0")

# Ensure INFO logs (including answer_timing) are emitted to stdout
logging.basicConfig(level=logging.INFO)

GATE_USERNAME = os.getenv("GATE_USERNAME", "")
GATE_PASSWORD = os.getenv("GATE_PASSWORD", "")

if GATE_PASSWORD:
    @app.middleware("http")
    async def basic_auth_middleware(request, call_next):
        if request.url.path == "/health":
            return await call_next(request)
        auth = request.headers.get("authorization")
        ok = False
        if auth and auth.startswith("Basic "):
            try:
                decoded = base64.b64decode(auth[6:]).decode("utf-8", errors="ignore")
                if ":" in decoded:
                    user, pwd = decoded.split(":", 1)
                    if GATE_USERNAME:
                        ok = (user == GATE_USERNAME and pwd == GATE_PASSWORD)
                    else:
                        ok = (pwd == GATE_PASSWORD)
            except Exception:
                ok = False
        if not ok:
            resp = Response(status_code=401)
            resp.headers["WWW-Authenticate"] = 'Basic realm="Restricted"'
            return resp
        return await call_next(request)

@app.get("/health")
async def health():
    checks = {"vertex": "unknown", "db": "unknown", "reranker": "unknown", "llm": "unknown"}
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

app.include_router(answer_router)
app.include_router(brief_router)
app.include_router(upload_router)
app.include_router(journal_router)

ui_root = Path("/app")
if (ui_root / "index.html").exists() and (ui_root / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(ui_root / "assets"), html=False), name="assets")
    @app.get("/")
    async def root_index():
        return FileResponse(str(ui_root / "index.html"))

@app.get("/favicon.ico")
async def favicon():
    icon_path = Path("/app/assets/favicon.ico")
    if icon_path.exists():
        return FileResponse(str(icon_path))
    return Response(status_code=204)

@app.post("/admin/fix_schema")
async def admin_fix_schema():
    before = []
    after = []
    try:
        with get_conn().cursor() as cur:
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='fragments'")
            before = [r[0] for r in cur.fetchall()]
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            cur.execute("ALTER TABLE fragments ADD COLUMN IF NOT EXISTS chunk_hash varchar(64)")
            cur.execute("ALTER TABLE fragments ADD COLUMN IF NOT EXISTS embedding_vec vector(768)")
            cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_frag_doc_chunk_idx ON fragments (doc_id, chunk_hash)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_fragments_vec ON fragments USING ivfflat (embedding_vec)")
            get_conn().commit()
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='fragments'")
            after = [r[0] for r in cur.fetchall()]
        return JSONResponse(content={"ok": True, "before": before, "after": after})
    except Exception as e:
        return JSONResponse(content={"ok": False, "error": str(e), "before": before, "after": after}, status_code=500)
