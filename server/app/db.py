import os
import psycopg
from pgvector.psycopg import register_vector

_conn = None

def get_conn():
    global _conn
    if _conn is None or _conn.closed:
        dsn = os.getenv("DATABASE_URL", "")
        if not dsn:
            raise RuntimeError("DATABASE_URL not set")
        _conn = psycopg.connect(dsn)
        register_vector(_conn)
    return _conn
