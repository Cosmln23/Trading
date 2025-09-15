from fastapi import APIRouter, UploadFile, File, Form
from typing import List
import hashlib
import os
import time
import logging

router = APIRouter(prefix="/api")

ALLOWED_EXT = {"pdf", "txt", "md", "docx", "csv"}

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), strategy: str = Form("A")):
    t0 = time.perf_counter()
    results = []
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
    try:
        logging.getLogger("app.upload").info(
            "upload_batch files=%s strategy=%s duration_ms=%s statuses=%s",
            len(results), strategy, int((time.perf_counter() - t0) * 1000), [r.get("status") for r in results]
        )
    except Exception:
        pass
    return results
