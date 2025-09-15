from fastapi import APIRouter, UploadFile, File, Form
from typing import List
import hashlib
import os
import time
import logging
import uuid
from .db import get_conn

router = APIRouter(prefix="/api")

ALLOWED_EXT = {"pdf", "txt", "md", "docx", "csv"}

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), strategy: str = Form("A")):
    t0 = time.perf_counter()
    results = []
    ingest_count = 0
    embedded_count = 0

    def map_collection(s: str) -> str:
        return "EQ_INV" if s == "A" else ("EQ_MOM_PEAD" if s == "B" else "OPT_INCOME")

    def split_text(text: str, max_chars: int = 3000, overlap: int = 400):
        text = text or ""
        chunks = []
        i = 0
        n = len(text)
        while i < n:
            j = min(n, i + max_chars)
            chunk = text[i:j]
            chunks.append(chunk)
            if j == n:
                break
            i = max(i + max_chars - overlap, i + 1)
        return chunks

    def vertex_embed_batch(texts):
        project = os.getenv("VERTEX_PROJECT_ID")
        location = os.getenv("VERTEX_LOCATION", "us-central1")
        model = os.getenv("EMBED_MODEL", "text-embedding-004")
        if not project:
            return None
        try:
            from vertexai import init
            from vertexai.language_models import TextEmbeddingModel
            init(project=project, location=location)
            mdl = TextEmbeddingModel.from_pretrained(model)
            embs = mdl.get_embeddings(texts)
            out = []
            for e in embs:
                vals = getattr(e, "values", None) or getattr(getattr(e, "embedding", None), "values", None)
                if vals is None:
                    out.append(None)
                else:
                    # L2 normalize
                    import math
                    norm = math.sqrt(sum(v*v for v in vals)) or 1.0
                    out.append([float(v)/norm for v in vals])
            return out
        except Exception:
            return None

    # Detect embedding column once
    emb_col = "embedding_vec"
    try:
        with get_conn().cursor() as cur:
            cur.execute("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name='fragments' AND column_name IN ('embedding_vec','embedding')
            """)
            cols = {r[0] for r in cur.fetchall()}
            if 'embedding_vec' in cols:
                emb_col = 'embedding_vec'
            elif 'embedding' in cols:
                emb_col = 'embedding'
            else:
                emb_col = None
    except Exception:
        emb_col = None
    for f in files:
        name = f.filename or "file"
        ext = (name.rsplit(".", 1)[-1].lower() if "." in name else "")
        if ext and ext not in ALLOWED_EXT:
            results.append({"name": name, "size": 0, "status": "rejected", "reason": "format neacceptat"})
            continue
        # compute hash to simulate dedup
        data = await f.read()
        size = len(data)
        file_hash = hashlib.sha256(data).hexdigest()
        # simple rule: if name or hash ends with '0' treat as dedup (demo)
        if name.lower().find("dup") >= 0 or file_hash.endswith("0"):
            results.append({"name": name, "size": size, "status": "dedup"})
        else:
            results.append({"name": name, "size": size, "status": "accepted"})
            # Ingest minimal: only for text-like files
            try:
                if ext in {"txt","md","csv","docx","pdf"}:
                    text = data.decode("utf-8", errors="ignore")
                    if ext == "csv":
                        text = " \n".join(line.strip() for line in text.splitlines() if line.strip())
                    elif ext == "docx":
                        from docx import Document
                        import io
                        doc = Document(io.BytesIO(data))
                        text = "\n".join(p.text for p in doc.paragraphs)
                    elif ext == "pdf":
                        from pypdf import PdfReader
                        import io
                        reader = PdfReader(io.BytesIO(data))
                        pages = []
                        for p in reader.pages:
                            try:
                                pages.append(p.extract_text() or "")
                            except Exception:
                                pages.append("")
                        text = "\n".join(pages)

                    collection = map_collection(strategy)
                    doc_id = f"upload:{name}"
                    chunks = split_text(text, max_chars=3500, overlap=500)
                    # Batch embeddings (size 32)
                    vectors = []
                    batch = 32
                    for s in range(0, len(chunks), batch):
                        part = vertex_embed_batch(chunks[s:s+batch]) or [None] * len(chunks[s:s+batch])
                        vectors.extend(part)
                    with get_conn().cursor() as cur:
                        for idx, (chunk, vec) in enumerate(zip(chunks, vectors)):
                            frag_id = uuid.uuid4().hex
                            # Dedup via chunk_hash
                            ch = hashlib.md5(chunk.encode('utf-8', errors='ignore')).hexdigest()
                            if emb_col is None or vec is None:
                                cur.execute(
                                    "INSERT INTO fragments (id, doc_id, collection, page, chunk_index, text, chunk_hash) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (doc_id, chunk_hash) DO NOTHING",
                                    (frag_id, doc_id, collection, None, idx, chunk[:4000], ch)
                                )
                            else:
                                cur.execute(
                                    f"INSERT INTO fragments (id, doc_id, collection, page, chunk_index, text, {emb_col}, chunk_hash) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (doc_id, chunk_hash) DO NOTHING",
                                    (frag_id, doc_id, collection, None, idx, chunk[:4000], vec, ch)
                                )
                            ingest_count += 1
                            if vec is not None:
                                embedded_count += 1
                        get_conn().commit()
            except Exception:
                # swallow ingest error; file remains accepted
                pass
    try:
        logging.getLogger("app.upload").info(
            "upload_batch files=%s strategy=%s duration_ms=%s statuses=%s ingest_count=%s embedded_count=%s",
            len(results), strategy, int((time.perf_counter() - t0) * 1000), [r.get("status") for r in results], ingest_count, embedded_count
        )
    except Exception:
        pass
    return results
