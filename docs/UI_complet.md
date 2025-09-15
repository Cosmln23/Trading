## UI Complet — Asistent Trading (V1)

Această specificație consolidează „PROMPT UNIC — Agent…” și §6 (NFR & UX) din README, mapate la componentele UI implementate.

### 1) Scope & Reguli HARD
- Trei tab‑uri separate: `EQ-INV`, `EQ-MOM/PEAD`, `OPT-INCOME` (no‑mix între strategii).
- Context‑Only: badge vizibil și mesaj clar; răspunsul se bazează strict pe pasaje citate.
- Citări obligatorii: `[n]` inline și secțiune „Surse” sub card.
- Fail‑safe: „Insuficient context” când `citations.length < 3`.
- Skeletons pentru încărcare; mesaje clare de eroare.

### 2) Structură UI
- Header global: brand, butoane (Daily Brief, Jurnal, Upload, Setări), toggle „Mock mode ON/OFF”.
- Tabs Strategii: selector `EQ-INV | EQ-MOM/PEAD | OPT-INCOME`, chips read‑only (K, N, τ, Reranker, MMR, Recency).
- Zona Q&A: formular întrebare; stări loading/eroare/insuficient; card răspuns cu Teză, Setup, Invalidare, Niveluri, Risc/Incertitudine, Surse, CTA „Trimite în Jurnal”.
- Modale: Daily Brief, Jurnal (form + listă + export CSV), Upload (dropzone + listă status), Setări (read‑only + Policy fix ON + Portofoliu CSV format).

### 3) Contracte date (rezumat)
- `/api/answer` POST → `{ answer:{thesis,setup,invalidation,levels,risk,uncertainty}, citations:[{doc_id,page,preview,url}] }`
- `/api/brief` GET → `{ macro:{stance,notes:[{text,citation}]}, ideas:{EQ_INV,EQ_MOM,OPT_INCOME}, calendar:[{time,type,symbol?,title}] }`
- `/api/journal` GET/POST → list/add (schema Jurnal)
- `/api/upload` POST → status per fișier: `accepted | dedup | rejected(reason)`
- `/api/settings` GET → `{K,N,tau,reranker,mmr,recency_boost,policy}`

### 4) Accesibilitate & UX
- ARIA pe butoane icon, focus rings, contraste suficiente, empty states.
- Fallback grațios: fără blocaje, opțiune de retry.

### 5) Implementare
- `index.html` conține markup complet (fără JS inline), Tailwind + lucide via CDN.
- JS separat: `assets/js/state.js`, `assets/js/mockData.js`, `assets/js/apiClient.js`, `assets/js/app.js`.
- Mock Mode toggle: controlează direcționarea apelurilor către mock sau fetch real (dacă există backend).


