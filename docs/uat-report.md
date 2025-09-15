# UAT Report — Template (V1)

> **Fișier:** `docs/uat-report.md`
> **Scop:** șablon standard pentru testarea UAT a **Cloud‑assisted RAG Trading Assistant (V1)** înainte de Go‑Live.

---

## 1) Metadate

* **Proiect:** Cloud‑assisted RAG Trading Assistant
* **Versiune testată:** V1.
* **Interval UAT:** `YYYY‑MM‑DD` → `YYYY‑MM‑DD`
* **Mediu:** `stage` (identic cu prod: da/nu)
* **Commit/Build:** `sha` / `tag`
* **Participanți:** Product Owner, QA Lead, Dev, Ops, Security

---

## 2) Scop & Domeniu

* **În‑scop:** UI taburi (**EQ‑INV**, **EQ‑MOM/PEAD**, **OPT‑INCOME**), **Daily Brief + Macro**, **Jurnal (CSV)**, **Upload**, **Setări**, **Reguli HARD** (no‑mix, Context‑Only, citări [n], prag τ, Reranker, MMR, Recency‑boost news).
* **În afara scopului:** orice extindere non‑V1.

---

## 3) Criterii de Intrare (Entry Criteria)

* [ ] Endpointurile răspund (health OK: Vertex, DB, Reranker, LLM)
* [ ] Corpus inițial încărcat per tab (minim set etalon)
* [ ] UI navigabil complet; Mock Mode **OFF** pe UAT
* [ ] KPI ținte definite (vezi §5)

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
| QA‑09 | Upload — accepted/dedup/rejected           |                    |          |
| QA‑10 | Jurnal — Add/Edit/Export CSV               |                    |          |
| QA‑11 | Latency — Query <3s, Brief <8s (p95)       |                    |          |
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

* **Query (p50/p95):** `x.xs / y.ys`
* **Daily Brief (p50/p95):** `x.xs / y.ys`
* **Observații:**

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

* **KPI‑uri atinse:** da/nu (detaliați)
* **Risc rezidual:**
* **Recomandare:** Go‑Live / Amană (cu motivare)

---

## 14) Acțiuni pentru Go‑Live

| # | Acțiune | Owner | Scadență | Status |
| - | ------- | ----- | -------- | ------ |
| 1 |         |       |          |        |

---

## 15) Semnături (Sign‑off)

* **Product Owner:** Nume, Dată, Semnătură
* **QA Lead:** Nume, Dată, Semnătură
* **Ops:** Nume, Dată, Semnătură
* **Security:** Nume, Dată, Semnătură
