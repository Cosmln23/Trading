# Plan implementare — 21/09/2025

## Context
- Serviciul `trading-api` este live pe Cloud Run, DB ok, IVFFLAT (lists=256), Observability drawer în UI, dashboard/alerte create.
- Gap-uri: Reranker, LLM real context-only, aliniere citări≥3 în backend, observabilitate persistentă (metrics), CORS strict, UAT evidențe.

## Obiective imediate (ordine execuție)
1) Integrare Reranker în `/api/answer` și păstrare N=3–5 (respect policy PRECISION).
2) Aplicare „Insuficient context” în backend când citări < 3 (aliniat cu UI).
3) LLM real (prompt strict, context-only), înlocuire răspuns demo.
4) Persistență observability events în DB + KPI extinse (precision@5, hallucination-rate) în `/observability/kpis`.
5) CORS restrâns la originea UI și secrete suplimentare în Secret Manager.
6) UAT: atașează capturi/loguri în `docs/uat-report.md` și semnături.

## Detaliere pași
- Reranker (/api/answer):
  - Env: `RERANK_URL`, `RERANK_API_KEY` (Secret Manager / env).
  - Flux: top‑K din pgvector → POST la reranker (query, candidates[text,id]) → scoruri → sortare desc → păstrezi top‑N 3–5 peste τ.
  - Observability: log `rerank_ms`, `candidates`, `kept`.

- Backend insuficient context (citări≥3):
  - După filtrare τ și (opțional) reranker, dacă `len(citations) < 3` ⇒ răspuns gol + citări [].

- LLM real (context-only):
  - Env: `LLM_URL`, `LLM_API_KEY`, `LLM_MODEL`, `LLM_TEMPERATURE`.
  - Prompt builder: doar pasaje (citări [n]) + instrucțiuni stricte „nu inventa; dacă lipsește context ⇒ mesaj insuficient”.

- Observability persistentă:
  - Tabel `events(component, ts, duration_ms, candidates, citations, insufficient, payload jsonb)` + agregare/minut în `metrics_minute`.
  - `/observability/kpis`: p50/p95 (5–15m), error%, rpm, plus precision@5 / hallucination‑rate (dacă există date QA).

- CORS & Secrete:
  - `ALLOWED_ORIGINS` → set exact domeniul UI.
  - Mută chei reranker/llm în secrete și folosește `--set-secrets` la deploy.

## Definition of Done
- `/api/answer` reordonează via Reranker; returnează N=3–5; „insuficient context” dacă <3 citări.
- Răspuns LLM real (temperatură 0–0.3), context-only; microcopy respectat.
- KPI live în drawer + dashboard; events persistente; p95 stabil.
- CORS strict; secrete gestionate în Secret Manager.
- `docs/uat-report.md` completat cu capturi; semnături pregătite.

## Next steps (astăzi)
- [ ] Integrare Reranker în `/api/answer` (env + cod + log + test 5–10 req).
- [ ] Aplicare prag citări≥3 în backend.
