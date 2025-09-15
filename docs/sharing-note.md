# Notițe: Partajare sigură cu un prieten (V1)

## Cea mai sigură variantă simplă (recomandat)
- Servești UI și API de pe același domeniu.
- Un singur host (ex. `app.domeniul-tau.ro`).
- UI static la rădăcină `/`.
- API sub `/api/*` (same-origin ⇒ fără CORS, mai puține probleme cu cookies).

## Checklist publicare (rapid & corect)
- Domeniu + HTTPS (TLS automat, ex. cu un reverse proxy).
- Same-origin routing: UI la `/`, backend la `/api`.
- Chei doar pe server (niciodată în JS din browser).

## Acces pentru prieten
- Minim: parolă la intrare (Basic Auth/"password gate").
- Mai bun: link de invitație (token "guest") care expiră, read-only.
- Rol "guest": dezactivează Upload și Setări; permite Q&A, Daily Brief, Jurnal (vizualizare).
- Spații separate de date: namespace dedicat prietenului (ca să nu amesteci corpusul tău).
- Limitare abuz: rate-limit pe `/api/*`, logări fără text integral (ID/hash).
- Mock Mode OFF pe producție; ON doar pentru demo.

## Ce vede prietenul
- Intri pe link, bagi parola / folosești linkul cu token → are acces la tab-uri, Daily Brief, Q&A cu citări.
- Nu poate încărca fișiere sau schimba setări.
