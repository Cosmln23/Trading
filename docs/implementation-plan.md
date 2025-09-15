# Implementation Plan — UI-only (V1)

## Scope
- Doar UI: 3 tab-uri (EQ-INV | EQ-MOM/PEAD | OPT-INCOME), Daily Brief, Jurnal, Upload, Setări.
- Respectă Regulile HARD: no‑mix, Context‑Only, citări obligatorii, insufficient <3 citări, skeletons/erori.

## Stack & Structură
- Tailwind + lucide (CDN). HTML semnatic.
- JS separat: `state.js`, `mockData.js`, `apiClient.js`, `app.js`.
- Docs: `UI_complet.md`, `data-contracts.md`, `qa-brief.md`, `runbook.md`, `architecture.md`.

## Etape
1. Scaffold `index.html` (markup complet, fără JS inline).
2. `state.js`: model de stare, mutații.
3. `mockData.js`: fixtures + delays (answer/brief/journal/upload/settings).
4. `apiClient.js`: switch mock/real, fetch helpers.
5. `app.js`: bindings, randare, stări (loading/error/insufficient), modale, CSV, upload.
6. Docs populate.
7. QA vizual conform `docs/qa-brief.md`.

## Criterii de acceptare
- Toate fluxurile funcționează în Mock Mode ON.
- Contractele de date vizual respectate.
- Accesibilitate de bază (ARIA, focus, contrast) și skeletons.
