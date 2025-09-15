# Architecture — UI Mock (V1)

## Overview
- Static single‑page UI: `index.html` + Tailwind + lucide (CDN).
- JS modular fără framework:
  - `assets/js/state.js`: stare globală + mutații.
  - `assets/js/mockData.js`: fixture‑e și delay-uri pentru demo.
  - `assets/js/apiClient.js`: rutează apeluri către mock sau `fetch` real.
  - `assets/js/app.js`: legături DOM, randare, handlers, modale.

## Flow
1. La load: mount icons → `getSettings()` → populate chips și Setări.
2. Q&A: submit → `postAnswer({question, collection})` → randare card sau stări error/insufficient.
3. Daily Brief: open modal → `getBrief()` → randare macro/idei/calendar.
4. Jurnal: open modal → `getJournal()`; submit → `postJournal()`; export CSV local.
5. Upload: select/drop → `postUpload(files, strategy)` → randare status pe fișier.

## Toggle Mock Mode
- `state.mockMode` controlează clientul: mock (default) vs. fetch real.
- Nu există persistență în mock; toate listele sunt volatiles.
