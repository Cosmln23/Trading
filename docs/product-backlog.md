# Product Backlog — Next Features

- Document Catalog (books vs news)
  - API: GET /api/documents?type=books|news (sursă: upload_history + fragments)
  - UI: listă persistată între refresh-uri, cu căutare și filtre

- Upload History in UI
  - Afișare ultimelor upload-uri (nume fișier, strategie, stats), link spre doc_id

- News Pipeline (zilnic)
  - Ingest separat de „books”; nu amestecă colecțiile
  - UI: tab/filtru dedicat news

- Chat Mode (LLM conversations)
  - API: /api/chat (POST mesaje, GET istoric, stocare în DB)
  - UI: interfață tip chat scrollabilă (istoric conversații + input continuu)

- Observability (extins)
  - Persist istoric conversații în events (component=chat)
  - KPI: utilizare chat, rata răspunsurilor cu citări

---

## Cerințe explicite (Cosmin)
- Persistență în UI după refresh pentru documente încărcate; catalog separat pentru cărți vs știri zilnice.
- Istoric upload vizibil în UI (books separate de news).
- Asistent LLM „chat” care:
  - Sugerează bazat pe cărți + cunoștințe încărcate.
  - Integrează știrile zilnice care influențează bursa.
  - Primește portofoliul și sugerează soluții cu explicații „de ce”.
  - Interfață chat scrollabilă (istoric conversații), nu doar un singur răspuns.

## Probleme observate (de remediat)
- „Deschide pasaj” deschidea aceeași pagină (rezolvat: pop-up dedicat cu doc/page/preview).
- „Trimite în Jurnal” arunca eroare (de verificat end-to-end pe UI + API /journal).
- Răspunsuri „Insuficient context” pe corpus mic (ameliorat: prag citări ≥1; τ configurabil din env).

## TODO concis (implementare)
1) API Document Catalog: GET /api/documents?type=books|news; sursă `upload_history` + `fragments` (doc_id, collection, created_at).
2) UI Catalog: listă căutabilă, persistentă între refresh-uri; secțiuni Books vs News.
3) UI Upload History: tabel în modal Upload (ultimele N înregistrări din `upload_history`).
4) News pipeline: strategie/colecție separată; UI filtru pentru news; nu se amestecă cu cărți.
5) API Chat: /api/chat (POST message; GET /api/chat/history?session=...); stocare în DB.
6) UI Chat: panou chat scrollabil cu istoric și input; legat de /api/chat.
7) „Trimite în Jurnal”: verificare și fix postare în /journal; confirmare UI.
