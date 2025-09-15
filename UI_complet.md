1) Obiectiv & Scope (V1)

Trei tab-uri separate (nu se combină în același răspuns):

EQ-INV — investiții acțiuni/ETF (orizont multi-ani)

EQ-MOM/PEAD — momentum + catalizatori de earnings (acțiuni)

OPT-INCOME — covered calls / cash-secured puts

Modul Macro în Daily Brief (calendar evenimente + evaluare regim: favorabil / neutru / nefavorabil).

Jurnal de decizii (CSV manual), inclus în UI.

Asumă că backendul există (RAG cu Vertex + pgvector, reranker ON). UI doar le consumă:

/api/answer (Q&A per strategie)

/api/brief (Daily Brief)

/api/upload (status ingestie fișiere)

/api/journal (list/add)

/api/settings (get/save)

2) Reguli HARD (respectate de UI)

Rutare per tab: întrebarea dintr-un tab interoghează doar colecția acelui tab.

Citări obligatorii: orice afirmație factuală din răspuns are [n]; sub răspuns apare lista „Surse” (doc/pagină/link/preview).

Fail-safe: dacă după filtrare rămân < 3 pasaje peste prag ⇒ afișează „Nu am context suficient”.

Bias = PRECISION: K = 16–24, N = 3–5, τ = 0.20, Reranker = ON, MMR = ON, Recency-boost doar pentru news (UI doar afișează; nu modifică).

Context-Only: UI afișează badge/policy că răspunsul e generat strict din pasaje citate.

3) Structură UI (pagini/panouri)
3.1 Header global

Tab selector: EQ-INV | EQ-MOM | OPT-INCOME

Butoane: Daily Brief, Jurnal, Upload, Setări

3.2 Tab Strategie (comun tuturor)

Input întrebare (un rând) + buton Răspunde.

Card Răspuns (doar dacă există context suficient):

Teză (max 3 propoziții) cu [citări] inline.

Setup (condiții), Invalidare, Niveluri (entry/stop/TP) — listă clară.

Risc & Incertitudine: text scurt (low/med/high).

CTA: „Trimite în Jurnal” — precompletează formularul cu teză/niveluri.

Surse (listă sub card): [1] doc_id • p.X • preview 240c • (link „Deschide pasaj”).

Stări: loading (skeleton), eroare rețea, „Insuficient context” (mesaj standard, vezi §6).

3.3 Daily Brief (08:00)

Regim piață (Macro): badge favorabil / neutru / nefavorabil + note scurte (CPI/NFP/FOMC/ECB, USD, real yields, vol proxy) cu citări.

Top 3 idei / strategie: scor + incertitudine + citări; click pe idee → deschide Card Răspuns.

Calendar evenimente (ziua curentă): earnings & macro (listă compactă).

3.4 Jurnal

Formular Add entry (câmpuri fixe):
timestamp, strategy(A/B/C), symbol, direction, entry, size, stop, tp, rationale, tags

Listă decizii recente: status (open/closed), PnL (dacă exit), R/R, link la răspunsul sursă.

Export CSV (schema de mai sus).

Validări blânde: avertizează dacă mărimea implică depășirea riscului/trade setat (nu bloca).

3.5 Upload

Drag&drop fișiere (cărți/rapoarte/știri) → Selectează strategia țintă (A/B/C) → arată status ingestie: acceptat / dedup / respins (motiv).

3.6 Setări

Retrieval (read-only sau editable după implementare): K, N, τ, Reranker ON, MMR ON, Recency-boost=News.

Policy: toggle Context-Only (fixat ON în V1; disable vizual).

Portofoliu CSV: format/ordonare câmpuri (conform Jurnal).

4) Contracte de date (fără cod; pentru mapare UI)

UI presupune aceste forme de răspuns (exemple de schemă, nu cod):

/api/answer (POST) → { answer: { thesis, setup, invalidation, levels, risk, uncertainty }, citations: [{label, doc_id, page, preview, url}] }

/api/brief (GET) → { macro: { stance, notes:[{text, citation}] }, ideas: { EQ_INV: [...], EQ_MOM: [...], OPT_INCOME: [...] }, calendar: [{time, type, symbol?, title}] }

/api/journal (GET/POST) → list/add pe schema Jurnal.

/api/upload (POST) → status pe fișiere: accepted | dedup | rejected(reason).

/api/settings (GET) → { K, N, tau, reranker:true, mmr:true, recency_boost:'news', policy:'context-only' }.

5) Micro-copy (obligatoriu în UI)

Insuficient context: „Nu am context suficient peste pragul de relevanță. Încarcă surse sau relaxează filtrele.”

Policy: „Răspuns generat strict din pasaje citate (Context-Only).”

Avertisment risc: „Sugestii, nu ordine. Respectă limitele de risc setate.”

6) NFR & UX

Latency țintă: Query < 3s, Daily Brief < 8s (afișează skeleton până la completare).

Auditabilitate: toate ideile au citări clicabile („Deschide pasaj”).

Accesibilitate: focus states, aria-labels, contraste suficiente.

Fallback grațios: mesaje clare pentru erori; fără blocaje.

7) Criterii de acceptare (QA)

100% răspunsuri afișează citări; niciun paragraf factual fără [n].

Nicio întrebare dintr-un tab nu trage rezultate din alt tab (no-mix).

„Insuficient context” apare când <3 pasaje peste τ.

Daily Brief conține Macro stance + Top 3 idei / strategie + Calendar, toate cu citări.

Jurnal: se poate adăuga intrare, lista se actualizează, Export CSV funcțional (schema fixă).