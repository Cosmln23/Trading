# QA Brief — UI (V1)

## Entry criteria
- UI se încarcă, Tailwind + lucide disponibile; Mock Mode ON.

## Teste cheie
- Tabs: schimbare tab evidențiază corect și resetează stările Q&A (no‑mix vizual).
- Q&A:
  - Submit întrebare cu „ok” → card cu `[n]` inline, Surse listate (≥3), badge risc/incertitudine, CTA Jurnal.
  - Submit „lowctx” → mesaj „Insuficient context”.
  - Submit alt text → mesaj eroare + buton „Reîncearcă”.
- Daily Brief: stance badge, note cu link „Deschide pasaj”, 3 idei/strategie, calendar populat, „Deschide răspuns” schimbă tab și interoghează.
- Jurnal: Add entry adaugă în listă; Export CSV descarcă fișier corect formatat.
- Upload: selectare fișiere → postUpload → status accepted/dedup/rejected vizibil; motiv pentru rejected.
- Setări: K, N, τ, Reranker, MMR, Recency populate; Context‑Only toggle disabled ON.

## Non‑funcționale
- Skeletons vizibile în stări de încărcare (Q&A, Brief, Journal, Calendar).
- Focus states pe butoane și controale; aria‑label pe butoane icon.

## Exit criteria
- Toate testele de mai sus PASS pe Chrome/Edge recent (desktop) cu Mock Mode ON.
