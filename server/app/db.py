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
        # Optional performance/session tuning
        try:
            probes = int(os.getenv("PGVECTOR_PROBES", "0") or 0)
        except Exception:
            probes = 0
        try:
            timeout_ms = int(os.getenv("DB_STATEMENT_TIMEOUT_MS", "0") or 0)
        except Exception:
            timeout_ms = 0
        with _conn.cursor() as cur:
            if probes > 0:
                try:
                    cur.execute("SET ivfflat.probes = %s", (probes,))
                except Exception:
                    pass
            if timeout_ms > 0:
                try:
                    cur.execute("SET statement_timeout = %s", (timeout_ms,))
                except Exception:
                    pass
    return _conn
