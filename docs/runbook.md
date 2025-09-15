# Runbook — UI Mock (V1)

## Rulare locală
1. Deschide `index.html` în browser (Chrome/Edge).
2. Confirmă în header că „Mock mode” este ON.

## Fluxuri de verificat rapid
- Q&A:
  - Introdu „ok” și apasă „Răspunde” → vezi card + citări (≥3).
  - Introdu „lowctx” → mesaj „Insuficient context”.
  - Introdu orice alt text → eroare rețea + „Reîncearcă”.
- Daily Brief: Deschide din header, verifică stance/idei/calendar, „Deschide răspuns”.
- Jurnal: Adaugă o intrare minimă; Export CSV; verifică formatul.
- Upload: Încarcă 2–3 fișiere, vezi status accepted/dedup/rejected.
- Setări: Valorile populate și Context‑Only fix ON (disabled).

## Toggle Mock Mode
- Comutatorul din header sau mobil (default ON).
- Când e OFF, UI încearcă `fetch` către rutele `/api/...` (dacă backend-ul este disponibil); altfel apar erori grațioase.

## Known limits
- Nu există persistență reală; Journal și Upload sunt in‑memory în mock.
- Nu există rutare URL; doar stare internă.
