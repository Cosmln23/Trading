# Bug Report — Template (V1)

> **Fișier:** `docs/bug-report.md`
> **Scop:** standardizare raportare defecte pentru **Cloud‑assisted RAG Trading Assistant (V1)**.

---

## 1) Identificare

* **ID:** `BUG‑YYYYMMDD‑###`
* **Titlu:** scurt, descriptiv
* **Status:** New / Triaged / In Progress / Blocked / Fixed (Pending QA) / Verified / Closed (Duplicate | Won’t Fix | As Designed)
* **Severitate (impact tehnic):** Critical / High / Medium / Low *(vezi §2)*
* **Prioritate (ordine execuție):** P0 / P1 / P2 / P3 *(vezi §2)*
* **Componentă:** UI / /api/answer / /api/brief / /api/upload / /api/journal / /api/settings / DB (pgvector) / Reranker / LLM / Infra
* **Mediu:** dev / stage / prod
* **Versiune / Build:** tag / commit `sha`
* **Reporter:** nume
* **Asignat:** nume
* **Dată/Oră:** `YYYY‑MM‑DD HH:MM TZ`

---

## 2) Definiții Severitate & Prioritate

| Severitate | Definiție                                             | Exemplu                                              |
| ---------- | ----------------------------------------------------- | ---------------------------------------------------- |
| Critical   | Funcționalitate esențială indisponibilă; risc de date | /api/answer down; citări lipsă în toate răspunsurile |
| High       | Funcție majoră afectată; workaround dificil           | Daily Brief nu încarcă calendarul                    |
| Medium     | Problemă limitată / UI necritică                      | mesaj „Insuficient context” nu respectă microcopy    |
| Low        | Cosmetic / minore                                     | mis‑alignment icon                                   |

| Prioritate | Definiție                                  |
| ---------- | ------------------------------------------ |
| P0         | Fix imediat (înainte de Go‑Live / blocant) |
| P1         | Fix în următorul release                   |
| P2         | Fix planificat                             |
| P3         | Backlog / nice‑to‑have                     |

---

## 3) Descriere

* **Rezumat:** 1–3 propoziții
* **Context:** ce încercai să faci; tab/strategie; Mock ON/OFF

---

## 4) Pași de Reproducere

1.
2.
3.

* **Rată reproducere:** 10/10 | 7/10 | aleator
* **Date test / Input:** (întrebare, fișiere upload, etc.)

---

## 5) Rezultat Așteptat vs. Actual

* **Așteptat:**
* **Actual:**
* **Diferență observată:**

---

## 6) Evidențe

* **Capturi/Video:** link
* **Loguri/Console:** fragment relevant (fără date sensibile)
* **Trace/Request ID:** dacă există

---

## 7) Arie Afectată

* **Tab/Strategie:** EQ‑INV | EQ‑MOM/PEAD | OPT‑INCOME
* **Endpointuri:** /api/answer | /api/brief | /api/upload | /api/journal | /api/settings
* **Impact utilizator:** blocant / major / moderat / minor
* **Impact KPI:** precision@5 / hallucination‑rate / latency / rate „insuficient context” / altele
* **Workaround disponibil:** da/nu (descrie)

---

## 8) Analiză & Cauză Rădăcină (după triere)

* **Tip cauză:** UI / API Contract / Retrieval / Reranker / LLM / Data (ingest) / Infra / Config / Security / Timeout / Altele
* **RCA scurt:** (ce, de ce, unde)

---

## 9) Fix & Verificare

* **Propunere fix:**
* **PR/Commit:** link
* **Test(e) adăugat(e):** unit / integration / e2e
* **Zone de regresie posibile:** (listează)
* **Instrucțiuni QA:** pași de validare
* **Rezultat QA:** Pass / Fail (detalii)

---

## 10) Timeline

* **Reportat:**
* **Triat:**
* **În lucru:**
* **Fixat:**
* **Verificat:**
* **Închis:**

---

## 11) Note & Linkuri

* Issue‑uri înrudite:
* Documentație: `docs/qa-brief.md`, `docs/data-contracts.md`, `README.md`

---

## 12) Șablon CSV (opțional)

> Pentru management rapid în foi de calcul, folosiți capetele de coloană de mai jos.

```
ID,Title,Status,Severity,Priority,Component,Environment,Version,Build,Reporter,Assignee,CreatedAt,UpdatedAt,ReproSteps,ReproRate,Expected,Actual,ImpactUser,ImpactKPI,AffectedAPIs,Screenshots,Logs,RootCauseType,FixPR,TestsAdded,RegressionAreas,QAResult
```
