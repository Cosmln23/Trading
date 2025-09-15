import os, psycopg, math
from pgvector.psycopg import register_vector
from vertexai import init
from vertexai.language_models import TextEmbeddingModel

dsn  = os.getenv("DATABASE_URL")
proj = os.getenv("VERTEX_PROJECT_ID")
loc  = os.getenv("VERTEX_LOCATION","us-central1")
model_name = os.getenv("EMBED_MODEL","textembedding-gecko@003")

init(project=proj, location=loc)
mdl = TextEmbeddingModel.from_pretrained(model_name)

with psycopg.connect(dsn) as conn:
    register_vector(conn)
    with conn.cursor() as cur:
        cur.execute("SELECT id, text FROM fragments WHERE embedding_vec IS NULL LIMIT 1000;")
        rows = cur.fetchall()
        for rid, txt in rows:
            if not txt: continue
            emb = mdl.get_embeddings([txt])[0]
            vals = getattr(emb, "values", None) or getattr(getattr(emb,"embedding",None),"values",None)
            if not vals: continue
            nrm = math.sqrt(sum(v*v for v in vals)) or 1.0
            vec = [v/nrm for v in vals]
            cur.execute("UPDATE fragments SET embedding_vec=%s WHERE id=%s", (vec, rid))
    conn.commit()
print("OK backfill")
