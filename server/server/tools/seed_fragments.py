import os
import psycopg

dsn = os.getenv("DATABASE_URL", "postgresql://postgres:changeme@localhost:5432/trading")
rows = [
    # EQ_INV (minim 3 fragmente)
    ("EQ_INV", "doc_EQINV_A", 1, 0, "EQ-INV: teză lungă despre investiții pe termen lung."),
    ("EQ_INV", "doc_EQINV_A", 1, 1, "EQ-INV: setup diversificare, cost mediu, riscuri macro."),
    ("EQ_INV", "doc_EQINV_A", 2, 2, "EQ-INV: niveluri indicative, cost total, rebalance."),
    # EQ_MOM_PEAD (opțional)
    ("EQ_MOM_PEAD", "doc_EQMOM_B", 3, 0, "EQ-MOM: momentum post-earnings, volum ridicat."),
    ("EQ_MOM_PEAD", "doc_EQMOM_B", 3, 1, "EQ-MOM: invalidare sub gap, risc controlat."),
    ("EQ_MOM_PEAD", "doc_EQMOM_B", 4, 2, "EQ-MOM: niveluri R/R, trailing stops."),
    # OPT_INCOME (opțional)
    ("OPT_INCOME", "doc_OPT_C", 5, 0, "OPT-INCOME: covered calls în regim volatilitate mică."),
    ("OPT_INCOME", "doc_OPT_C", 5, 1, "OPT-INCOME: puturi cash-secured aproape de suport."),
    ("OPT_INCOME", "doc_OPT_C", 6, 2, "OPT-INCOME: scadențe și roll logic.")
]

with psycopg.connect(dsn) as conn:
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO fragments (id, doc_id, collection, page, chunk_index, text)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """,
            [(f"{c}_{i}", d, c, p, k, t) for i, (c, d, p, k, t) in enumerate(rows, start=1)]
        )
    conn.commit()
print("OK: seed inserat.")
