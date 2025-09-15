# Data Contracts (UI assumptions)

## /api/settings (GET)
Response:
```json
{
  "K": 20,
  "N": 4,
  "tau": 0.2,
  "reranker": true,
  "mmr": true,
  "recency_boost": "news",
  "policy": "context-only"
}
```

## /api/answer (POST)
Request:
```json
{ "question": "string", "collection": "EQ_INV|EQ_MOM_PEAD|OPT_INCOME" }
```
Success response:
```json
{
  "answer": {
    "thesis": "string",
    "setup": "string",
    "invalidation": "string",
    "levels": "entry 100, stop 95, TP 112",
    "risk": "low|med|high",
    "uncertainty": "low|med|high"
  },
  "citations": [
    { "doc_id": "string", "page": 1, "preview": "string", "url": "string" }
  ]
}
```
Insufficient context response (UI rule if citations < 3):
```json
{ "answer": {"thesis":"","setup":"","invalidation":"","levels":"","risk":"—","uncertainty":"—"}, "citations": [] }
```

## /api/brief (GET)
Response:
```json
{
  "macro": { "stance": "favorabil|neutru|nefavorabil", "notes": [{ "text": "", "citation": {"url": ""} }] },
  "ideas": {
    "EQ_INV": [{ "text": "", "score": 0.75, "uncertainty": "low|med|high", "citations": [{"url": ""}] }],
    "EQ_MOM": [{ "text": "", "score": 0.65, "uncertainty": "med", "citations": [{"url": ""}] }],
    "OPT_INCOME": [{ "text": "", "score": 0.60, "uncertainty": "low", "citations": [{"url": ""}] }]
  },
  "calendar": [{ "time": "HH:MM", "type": "macro|earnings", "symbol": "AAPL", "title": "" }]
}
```

## /api/journal (GET/POST)
GET Response: `Entry[]`
```json
[{ "timestamp":"", "strategy":"A|B|C", "symbol":"", "direction":"long|short", "entry":0, "size":0, "stop":0, "tp":0, "rationale":"", "tags":"", "status":"open|closed", "rr":1.2, "pnl":0, "answer_id":"optional" }]
```
POST Request: same shape (fields optional)

## /api/upload (POST)
FormData: files[], strategy=A|B|C
Response:
```json
[
  { "name":"file.pdf", "size":123, "status":"accepted" },
  { "name":"file2.pdf", "size":456, "status":"dedup" },
  { "name":"file3.pdf", "size":789, "status":"rejected", "reason":"format neacceptat" }
]
```


