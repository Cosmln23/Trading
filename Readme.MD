# RAG OCR pipeline — scan carte → embeddings → FAISS (offline) + hook pentru cloud

## 0) Observații-cheie
- Un **scan** = imagini. Ca să devină căutabil pentru RAG, ai nevoie de **OCR** + **chunking** + **embeddings** + **index** (vector DB).
- Recomandat: **OCR cu text-layer** (ex: `ocrmypdf`) → extragere text rapidă cu PyMuPDF.
- Pentru **online**, păstrezi exact același flux (OCR → split → embeddings), dar înlocuiești `embed_local()` cu apelul la providerul de embeddings și faci **upsert** în Vector DB gestionat (Pinecone/Weaviate/Qdrant/pgvector).

---

## 1) Instalare (offline, Windows/Linux/macOS)

### Dependențe sistem
- Instalează **Tesseract OCR** (necesar pentru limbile `ron`, `eng`). Asigură-te că pachetul de limbă română este instalat.
- (Opțional, recomandat) Instalează **Poppler** dacă vrei să folosești `pdf2image` (noi folosim PyMuPDF, deci nu e obligatoriu).

### Python packages
```bash
pip install "sentence-transformers>=3.0" faiss-cpu "pymupdf>=1.23" pillow pytesseract ocrmypdf
```

### Verificare limbă Tesseract (Windows)
- Asigură-te că ai `ron.traineddata` în folderul `tessdata` al Tesseract.
- Dacă e nevoie, setează `TESSDATA_PREFIX` în environment.

---

## 2) OCR cu text-layer (rapid)
Dacă ai un PDF **scanat** (imagini-only), rulează:

```bash
ocrmypdf --language ron+eng --jobs 4 --optimize 1 input.pdf output_ocr.pdf
```

Rezultatul `output_ocr.pdf` va avea **text-layer** pagină cu pagină. Apoi extragi textul cu PyMuPDF **rapid**, fără OCR suplimentar.

---

## 3) Ingest (offline) — `ingest.py`

> Creează embedding-uri local și index FAISS. Salvează și metadatele pentru citări.

```python
# ingest.py
import json, os, re, math
from pathlib import Path
import numpy as np
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import faiss
import pytesseract
from PIL import Image

# ---------- Config ----------
CHUNK_SIZE = 1600          # ~caractere (aprox 300-500 tokeni, în funcție de text)
CHUNK_OVERLAP = 200
EMBED_MODEL = "gte-base"   # alternativ: "all-MiniLM-L6-v2" (mai mic)

# ---------- Utils ----------

def clean_text(t: str) -> str:
    t = re.sub(r"\s+", " ", t).strip()
    return t


def split_into_chunks(text: str, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + size)
        chunk = text[start:end]
        # extinde la capăt de propoziție dacă posibil
        if end < n:
            m = re.search(r"[\.!?]\s", text[end:end+200])
            if m:
                end = end + m.end()
                chunk = text[start:end]
        chunks.append(chunk)
        start = max(end - overlap, end) if end < n else end
    return [c for c in (s.strip() for s in chunks) if c]


def page_text_or_ocr(doc, pno: int, lang="ron+eng") -> str:
    page = doc.load_page(pno)
    t = page.get_text("text") or ""
    if len(t.strip()) >= 30:
        return t
    # fallback OCR pe imaginea paginii
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x pentru claritate
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    ocr = pytesseract.image_to_string(img, lang=lang)
    return ocr


# ---------- Main ingest ----------

def ingest_pdf(pdf_path: str, out_dir: str, doc_id: str):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # 1) Load PDF
    doc = fitz.open(pdf_path)

    # 2) Extract text per page
    pages = []
    for pno in range(len(doc)):
        txt = clean_text(page_text_or_ocr(doc, pno))
        pages.append({"page": pno + 1, "text": txt})

    # 3) Build chunks with metadata
    records = []
    for p in pages:
        if not p["text"]:
            continue
        chunks = split_into_chunks(p["text"])  # char-based simple split
        for i, ch in enumerate(chunks):
            records.append({
                "id": f"{doc_id}_p{p['page']:04d}_c{i:03d}",
                "doc_id": doc_id,
                "page": p["page"],
                "chunk_index": i,
                "text": ch
            })

    # 4) Embed (local)
    model = SentenceTransformer(EMBED_MODEL)
    texts = [r["text"] for r in records]
    # normalize pentru cosine/IP
    embs = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)

    # 5) FAISS index (cosine via inner product pe vectori normalizați)
    d = embs.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embs.astype("float32"))

    # 6) Persist
    faiss.write_index(index, str(out / "index.faiss"))
    np.save(out / "embeddings.npy", embs)
    with open(out / "meta.jsonl", "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"OK: {len(records)} chunks, dim={d}. Artifacts in {out}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", help="path la PDF (ideal OCR cu text-layer)")
    ap.add_argument("out", help="folder ieșire (index + meta)")
    ap.add_argument("--doc-id", default="carte")
    args = ap.parse_args()
    ingest_pdf(args.pdf, args.out, args.doc_id)
```

---

## 4) Căutare (offline) — `query.py`

```python
# query.py
import json
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

ART_DIR = Path("./artifacts")  # schimbă după nevoie
EMBED_MODEL = "gte-base"

# încarcă meta
META = []
with open(ART_DIR / "meta.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        META.append(json.loads(line))

# încarcă index
index = faiss.read_index(str(ART_DIR / "index.faiss"))
model = SentenceTransformer(EMBED_MODEL)


def search(query: str, k=5):
    q = model.encode([query], normalize_embeddings=True, convert_to_numpy=True).astype("float32")
    D, I = index.search(q, k)
    hits = []
    for rank, idx in enumerate(I[0]):
        r = META[idx]
        hits.append({
            "rank": rank + 1,
            "score": float(D[0][rank]),
            "id": r["id"],
            "doc_id": r["doc_id"],
            "page": r["page"],
            "chunk_index": r["chunk_index"],
            "text": r["text"][:400] + ("…" if len(r["text"]) > 400 else "")
        })
    return hits


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "procedură concediu de odihnă"
    for h in search(q, k=5):
        print(f"[{h['rank']}] p.{h['page']} score={h['score']:.3f} → {h['text']}")
```

---

## 5) Integrare „online” (schemă)
Păstrezi pașii 1–3 (OCR, split). În loc de `SentenceTransformer` local, apelezi **endpointul de embeddings** (ex. Google/Vertex) și faci upsert în vector DB gestionat.

### Pseudocod (Python) – `embed_cloud(text)`
```python
import requests

def embed_cloud(text: str) -> list[float]:
    url = os.environ["EMBED_URL"]  # endpointul providerului
    headers = {"Authorization": f"Bearer {os.environ['API_KEY']}", "Content-Type": "application/json"}
    payload = {"input": text, "model": os.environ.get("EMBED_MODEL", "text-embedding-xxx")}
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["data"][0]["embedding"]  # adaptează la schema providerului
```

### Upsert exemplu (Pinecone – schemă generică)
```python
from pinecone import Pinecone
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"]) ; idx = pc.Index(os.environ["PINECONE_INDEX"])

# vectors: list of {id, values, metadata}
idx.upsert(vectors=[
  {"id": rec["id"], "values": embed_cloud(rec["text"]), "metadata": {"doc_id": rec["doc_id"], "page": rec["page"], "chunk_index": rec["chunk_index"]}}
  for rec in records
])
```

---

## 6) Bune practici
- **Legal**: respectă drepturile de autor; nu indexa materiale fără drept.
- **Calitate OCR**: scanează la **300–400 dpi**, deskew; `--language ron+eng` pentru termeni amestecați.
- **Chunking**: 500–800 tokeni efectivi (char ~ 1500–2000); overlap 100–200.
- **Normalize embeddings** → cosine/IP.
- **Reranking**: pentru calitate, adaugă un cross-encoder (ex. `bge-reranker`) la query-time.
- **Versionare**: `doc_id`, `version`, `page`, `chunk_index`, `hash` în metadata.
- **Fallback**: dacă recall e mic, răspunde explicit că nu există context relevant.



---

## 15) Delivery Checklist (end‑to‑end)
**Scop:** minimizarea riscului de eșec prin pași clari, verificabili.

1. **Scope lock (V1):** A/B/C strategii confirmate · Bias **PRECISION** · **Daily Brief=ON** · **CSV portofoliu** · **Context‑Only=ON**.
2. **Secret management:** inventar variabile (§3.1), separă **dev/stage/prod**, rotație chei, acces minim (RBAC).
3. **GCP setup:** proiect → Vertex AI activ → service account + roluri minime → storage pentru artefacte.
4. **Cloud SQL (Postgres):** instanță + firewall/VPC → instalare **pgvector** → schema tabele (§4.1–4.3) → indexuri → backup & **PITR**.
5. **Reranker:** alege provider → setează **RERANK_URL/KEY** → healthcheck (200 OK, latency stabilă).
6. **LLM provider:** model + **temperature 0–0.3** + limită tokens → parametri cost/ratelimiting → healthcheck.
7. **Retrieval policy:** K=16–24 · N=3–5 · **τ=0.20** · **MMR=ON** · **recency‑boost=news** · router pe tab (no‑mix).
8. **Corpus curation:** selectează cărți/ghiduri/rapoarte per tab → **quality_score** (1–5) → whitelist surse.
9. **Ingestie:** OCR (300–400 dpi, ron+eng) → curățare → split (500–800 tkn, ovlp 100) → hashing/dedup → versionare → logging.
10. **Încărcare inițială:** upsert în pgvector pe namespaces (`EQ-INV`, `EQ-MOM`, `OPT-INCOME`) → verifică număr fragmente/colecție.
11. **Contracte API:** confirmă forme răspuns (§4.4) pentru `/answer`, `/brief`, `/upload`, `/journal`, `/settings` → mesaje de eroare standard.
12. **UI prototip:** taburi + **Daily Brief** + **Jurnal** + **Upload** + **Setări** → stări loading/empty/error + microcopy (§5–6).
13. **Set etalon QA:** 20 întrebări/anotări/tab + 5 cazuri „insuficient context”/tab + 10 evenimente macro etichetate.
14. **Testare funcțională:** rutare per tab, citări obligatorii, prag τ, reranker, MMR, recency‑boost, upload & status, jurnal & export.
15. **Testare performanță:** **query <3s**, **Brief <8s** (mediana, p95) sub încărcare rezonabilă.
16. **Securitate:** loguri fără text integral; doar ID/hash; acces DB cu rol minim; verifică expunerea endpointurilor.
17. **Observabilitate:** metrice (precision@5, hallucination‑rate, latency), dashboard + alerte praguri.
18. **Runbook & SOP:** ritual 07:30/08:00/17:00, fallback (degradare grațioasă), plan rollback.
19. **UAT (1 săpt.):** pe date reale; colectează bug‑uri/derapaje KPI; remediază.
20. **Go/No‑Go:** checklist acceptare (§8) semnat → **Launch** → monitorizare strânsă primele 7 zile.

---

## 16) QA Brief (scurt, acționabil)
**Obiectiv:** validarea criteriilor de acceptare și a gard‑rail‑urilor anti‑halucinații.

### 16.1 Mediu & intrări
- **Mediu:** stage identic cu prod (chei separate). Instrumentare latency/loguri activă.
- **Set etalon:** conform §15.13 (per tab + macro + insuficient context).
- **Entry criteria:** toate endpointurile răspund; corpus inițial încărcat; UI complet navigabil.

### 16.2 Teste cheie (ID → descriere → rezultat așteptat)
- **QA‑01 Rutare per tab:** întrebare în **EQ‑MOM** → citări doar din `EQ-MOM`. **No‑mix**.
- **QA‑02 Citări obligatorii:** orice afirmație factuală are **[n]** + listă **Surse** sub răspuns.
- **QA‑03 Prag τ:** pasaje sub **0.20** nu apar; dacă rămân <3 → **„Insuficient context”**.
- **QA‑04 Reranker:** calitatea ordonării ↑ vs. brute (verificare pe întrebări ambigue).
- **QA‑05 MMR/diversitate:** top‑N nu conține duplicate evidente/near‑duplicate.
- **QA‑06 Recency‑boost (news):** știrea recentă > material vechi la întrebare identică.
- **QA‑07 Daily Brief Macro:** afișează *favorabil/neutru/nefavorabil* cu **citări** la eveniment/pasaj.
- **QA‑08 Daily Brief Idei:** top 3/strategie conțin citări + incertitudine; click deschide cardul răspuns.
- **QA‑09 Upload:** fișier mapat la strategie → status **accepted/dedup/rejected** corect.
- **QA‑10 Jurnal:** Add/Edit; listă actualizată; **Export CSV** produce exact schema (§4.2).
- **QA‑11 Latency:** **query <3s**, **Brief <8s** (p50/p95). Afișare skeleton până la completare.
- **QA‑12 Eroare rețea:** UI afișează mesaj clar; fără crash; retry manual disponibil.
- **QA‑13 Securitate loguri:** nu apare text integral din surse; doar ID/hash.
- **QA‑14 Ambiguitate/Adversarial:** întrebări vagi → răspuns „Nu am context suficient” (fără improvizații).
- **QA‑15 I18N (opțional):** UI stabil cu limba RO; etichete/microcopy corecte.

### 16.3 Metrici & praguri de acceptare
- **precision@5 ≥ 0.70** (pe set etalon per tab).
- **hallucination‑rate ≤ 1%** (propoziții fără citări valide).
- **Latency p95:** query ≤ 3s; Brief ≤ 8s.

### 16.4 Raportare & semnare
- **Template raport:** ID test · status (Pass/Fail) · note · capturi · log ref · timp execuție.
- **Daily QA summary:** număr teste rulate/picate; buglist prioritar; trend KPI.
- **Exit criteria:** toate testele critice Pass; KPI în prag; bug‑uri rămase doar „minor”.
- **Sign‑off:** Product Owner · QA Lead · Ops · Security.

