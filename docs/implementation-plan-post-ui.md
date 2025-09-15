# Implementation Plan — Post‑UI to 100% Functional (V1)

> **Scope:** După livrarea UI‑only, finalizează back‑endul și integrarea până la produs funcțional conform README (RAG cloud‑assisted: Vertex + pgvector, Reranker ON, bias PRECISION, Daily Brief, Jurnal CSV).
>
> **Invariante (HARD):** No‑mix între strategii; Context‑Only; citări obligatorii [n]; K=16–24, N=3–5, τ=0.20, Reranker=ON, MMR=ON, Recency‑boost=news.

---

## Faza 0 — Baseline & Config

**Obiectiv:** cadru stabil pentru integrare.

* [ ] Confirmați .env (vezi README §3.1) pe **dev/stage/prod**.
* [ ] Service account & roluri minime (Vertex, Cloud SQL).
* [ ] Cloud SQL Postgres up; **pgvector** instalat; migrații tabele `fragments`, `journal`, `events`.
* **Artefacte:** `.env.*`, diagrame acces.
* **DOD:** health‑check DB OK; `PGVECTOR_DIM` setat; conexiune securizată.

## Faza 1 — API Contracts Freeze

**Obiectiv:** contracte stabile între UI și BE.

* [ ] Îngheață schemele: `/api/answer`, `/api/brief`, `/api/upload`, `/api/journal`, `/api/settings` (vezi README §4.4).
* [ ] Mock orchestrat în UI respectă exact contractele.
* **DOD:** docs/data‑contracts.md semnat; UI‑mock = verde.

## Faza 2 — /api/settings + Health

**Obiectiv:** expune setările și starea sistemului.

* [ ] `/api/settings` (read‑only în V1) returnează K/N/τ, reranker/mmr/recency, policy.
* [ ] `/health` pentru Vertex, DB, Reranker, LLM.
* **Artefacte:** document „health matrix”.
* **DOD:** UI citește setările reale; health returnează 200 și timpii.

## Faza 3 — Retrieval Core & /api/answer

**Obiectiv:** răspuns context‑only cu citări.

* [ ] Conector **Vertex embeddings** (text→vector; normalize L2).
* [ ] Retriever **pgvector** (namespace=tab; hybrid dense+BM25 dacă disponibil; fallback dense).
* [ ] **Reranker ON** (serviciu extern) — reordonează top‑K; păstrează **top‑N 3–5**.
* [ ] **Prag τ=0.20**; dacă <3 pasaje valide ⇒ răspuns „Insuficient context”.
* [ ] **Prompt builder** context‑only; citări [n] în text + listă Surse (doc/pagină/link/preview).
* [ ] Integrare **LLM** (temperatură 0–0.3).
* **Artefacte:** diagrame flux; exemple request/response reale.
* **DOD:** QA: QA‑01..QA‑06, QA‑11 Pass (vezi README §16.2).

## Faza 4 — /api/brief (Daily Brief + Macro)

**Obiectiv:** Brief la 08:00 cu stance macro, idei, calendar.

* [ ] Ingest „calendar” (earnings/macro) în `events` (schemă minimă).
* [ ] Reguli simple **macro stance** (favorabil/neutru/nefavorabil) + citări.
* [ ] Generare **Top 3 idei/strategie** (folosește același pipeline ca /answer, dar cu prompt predefinit).
* **DOD:** QA‑07..QA‑08 Pass; timpi <8s.

## Faza 5 — Ingest & /api/upload

**Obiectiv:** adăugare surse cu mapare la strategie.

* [ ] Endpoint acceptă fișier + strategie; validează MIME; idempotent (hash).
* [ ] Pipeline: OCR (dacă scan), curățare, **split 500–800 tkn, ovlp 100**, embeddings Vertex, **upsert** în `fragments` (namespace corect), metadata completă.
* [ ] Status: `accepted | dedup | rejected(reason)`.
* **DOD:** QA‑09 Pass; intrări corecte în DB; dedup funcțional.

## Faza 6 — Jurnal & CSV

**Obiectiv:** jurnal operativ + export.

* [ ] `/api/journal` list/add conform schemei (timestamp, strategy, symbol, direction, entry, size, stop, tp, exit?, PnL?, risk_R, rationale, tags).
* [ ] Export CSV cu escaping corect.
* **DOD:** QA‑10 Pass; fișier CSV validat cu valori reale.

## Faza 7 — Security & Policy

**Obiectiv:** confidențialitate și predictibilitate.

* [ ] RBAC minim; chei gestionate; .env separat per mediu.
* [ ] Loguri fără text integral; doar ID/hash; redactarea erorilor.
* [ ] **Policy Context‑Only** impus la nivel de server (nu doar UI).
* **DOD:** revizie security; teste negative (injection/oversized input) Pass.

## Faza 8 — Observabilitate & KPI

**Obiectiv:** măsurare calitate & latență.

* [ ] Metrice: precision@5, hallucination‑rate, latency (p50/p95), rate „Insuficient context”.
* [ ] Dashboard + alerte praguri.
* **DOD:** praguri atinse: precision@5≥0.70; hallucination‑rate≤1%; query<3s p95; Brief<8s p95.

## Faza 9 — Performanță & Cost

**Obiectiv:** SLA UI și cost control.

* [ ] Cache scurt pentru embeddings identice; batch la ingest.
* [ ] Concurență testată (utilizator unic intens); p95 sub ținte.
* **DOD:** raport TCO estimativ; teste încărcare Pass.

## Faza 10 — UAT & Go‑Live

**Obiectiv:** validare finală pe date reale.

* [ ] UAT 1 săptămână (set etalon + folosire reală).
* [ ] Bug bash; remediere.
* [ ] Go/No‑Go pe criterii acceptare (README §8).
* **DOD:** semnături: Product, QA, Ops, Security.

---

## Risk Register (selectiv)

* **Corpus zgomotos:** mitigare — whitelist + quality_score; dedup/hashing.
* **Contradicții între strategii:** separare strictă pe namespace; cross‑check doar în raport, nu în prompt.
* **Recency bias:** recency‑boost moderat; fallback „nu știu”.
* **Dependință de un serviciu (LLM/Reranker):** health‑checks; degrade grațios; timeouts + retry policy.

---

## Hand‑off & Artefacte finale

* **Docs:** README, architecture.md, data‑contracts.md, QA‑brief.md, runbook.md, **implementation‑plan.md** (acest fișier).
* **Checklists semnate:** Delivery (§15) + QA (§16) din README.
* **Raport UAT & KPI:** rezultate măsurate vs praguri.
