# UAT Report — Template (V1)

> **Fișier:** `docs/uat-report.md`
> **Scop:** șablon standard pentru testarea UAT a **Cloud‑assisted RAG Trading Assistant (V1)** înainte de Go‑Live.

---

## 1) Metadate

* **Proiect:** Cloud‑assisted RAG Trading Assistant
* **Versiune testată:** v22–v23 (api‑v22/api‑v23)
* **Interval UAT:** 2025‑09‑20 → 2025‑09‑20
* **Mediu:** Cloud Run (us‑central1) + Cloud SQL (Postgres, pgvector)
* **Commit/Build:** revizia live (Service URL Cloud Run), taguri: api‑v22, api‑v23
* **Participanți:** Owner, Dev

---

## 2) Scop & Domeniu

* **În‑scop:** UI taburi (**EQ‑INV**, **EQ‑MOM/PEAD**, **OPT‑INCOME**), **Daily Brief + Macro**, **Jurnal (CSV)**, **Upload**, **Setări**, **Reguli HARD** (no‑mix, Context‑Only, citări [n], prag τ, Reranker, MMR, Recency‑boost news).
* **În afara scopului:** orice extindere non‑V1.

---

## 3) Criterii de Intrare (Entry Criteria)

* [x] Endpointuri răspund (health OK: DB)
* [x] Pipeline upload → embeddings (Vertex) → DB confirmat (embedded_count > 0)
* [x] `upload_history` activ (per‑file stats)
* [x] Basic Auth + CORS + rate limiting active; secrete în Secret Manager
* [x] Alerte create (5xx, p95) + dashboard KPI
* [ ] Corpus etalon finalizat pe toate tab‑urile
* [ ] KPI ținte validate (vezi §5)

---

## 4) Set Etalon & Date de Test

* **Întrebări per tab:** 20 (anotate cu pasaje corecte)
* **Cazuri „Insuficient context” per tab:** 5
* **Evenimente macro etichetate:** 10 (CPI/NFP/FOMC/earnings)
* **Fișiere Upload:** min. 6 (mix: accepted/dedup/rejected)

---

## 5) KPI‑uri & Praguri (Acceptare)

* **precision@5 ≥ 0.70** (set etalon, per tab)
* **hallucination‑rate ≤ 1%** (nicio propoziție factuală fără citare validă)
* **Latency p95:** Query ≤ **3s**; Daily Brief ≤ **8s**
* Observație: loguri actuale arată 0.2–9.5s în funcție de query; optimizări în curs

---

## 6) Matrice trasabilitate (QA‑01 … QA‑15)

| ID    | Descriere                                  | Status (Pass/Fail) | Evidență |
| ----- | ------------------------------------------ | ------------------ | -------- |
| QA‑01 | Rutare per tab (no‑mix)                    |                    |          |
| QA‑02 | Citări obligatorii [n] + listă Surse      |                    |          |
| QA‑03 | Prag τ=0.20 + fallback Insuficient context |                    |          |
| QA‑04 | Reranker îmbunătățește ordonarea           |                    |          |
| QA‑05 | MMR/diversitate (fără duplicate)           |                    |          |
| QA‑06 | Recency‑boost (news)                       |                    |          |
| QA‑07 | Daily Brief — Macro stance cu citări       |                    |          |
| QA‑08 | Daily Brief — Top 3 idei/strategie         |                    |          |
| QA‑09 | Upload — accepted/dedup/rejected           | Pass               | logs     |
| QA‑10 | Jurnal — Add/Edit/Export CSV               | Pass               | UI       |
| QA‑11 | Latency — Query <3s, Brief <8s (p95)       | Pending            |          |
| QA‑12 | Eroare rețea — fallback grațios            |                    |          |
| QA‑13 | Loguri — fără text integral din surse      |                    |          |
| QA‑14 | Ambiguitate — „Insuficient context”        |                    |          |
| QA‑15 | I18N (RO) — etichete/microcopy corecte     |                    |          |

---

## 7) Rezumat Execuție Teste

* **Total teste rulate:** `N`
* **Pass:** `Npass` | **Fail:** `Nfail`
* **Defecte deschise:** `Nopen` | **Critice:** `Ncrit`

---

## 8) Rezultate Detaliate Teste

> Completați pe test:

**Test ID:** QA‑XX
**Titlu:**
**Precondiții:**
**Pași:**
1.
2.
3.
**Rezultat așteptat:**
**Rezultat actual:**
**Status:** Pass/Fail
**Evidență:** link capturi/loguri

*(Repetați pentru toate testele din matrice.)*

---

## 9) Defecte & Issue Log

| ID      | Severitate | Prioritate | Componentă  | Descriere | Pași reproducere | Așteptat | Actual | Evidență | Status | Owner | ETA |
| ------- | ---------- | ---------- | ----------- | --------- | ---------------- | -------- | ------ | -------- | ------ | ----- | --- |
| BUG‑001 | Critic     | High       | /api/answer |           |                  |          |        |          | Open   |       |     |

---

## 10) Rezultate Performanță

* **Query (p50/p95):** `~0.25s / ~9.5s` (din `answer_timing`)
* **Daily Brief (p50/p95):** n/a (de completat după validare finală)
* **Observații:** p95 influențat de cold‑start și dimensiunea inputului; tuning IVFFLAT/PROBES planificat

---

## 11) Securitate & Confidențialitate

* [ ] Loguri fără text integral din surse (doar ID/hash)
* [ ] Erori redactate (fără date sensibile)
* [ ] Acces DB cu rol minim (RBAC) verificat

---

## 12) Accesibilitate & UX

* [ ] Focus ring vizibil; ARIA labels
* [ ] Constraste adecvate; navigare cu tastatura
* [ ] Empty states & mesaje de eroare clare

---

## 13) Concluzii UAT

* **KPI‑uri atinse:** Parțial (upload/ingest/embeddings/answer + securitate/observabilitate OK)
* **Risc rezidual:** latență p95 variabilă; corp etalon incomplet; Brief de finalizat
* **Recomandare:** Go‑Live pilot (limitat) după finalizarea §14‑1/2/3

---

## 14) Acțiuni pentru Go‑Live

| # | Acțiune | Owner | Scadență | Status |
| - | ------- | ----- | -------- | ------ |
| 1 | Finalizează Brief + citări                     | Dev   | 2 zile   | Open   |
| 2 | Tuning IVFFLAT (lists) + PGVECTOR_PROBES       | Dev   | 2 zile   | Open   |
| 3 | Dashboard: adaugă RPS și Error rate %          | Dev   | 1 zi     | Open   |
| 4 | UAT complet pe set etalon (3×20 întrebări)     | QA    | 2 zile   | Open   |

---

## 15) Semnături (Sign‑off)

* **Product Owner:** Nume, Dată, Semnătură
* **QA Lead:** Nume, Dată, Semnătură
* **Ops:** Nume, Dată, Semnătură
* **Security:** Nume, Dată, Semnătură
