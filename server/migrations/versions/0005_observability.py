from alembic import op
import sqlalchemy as sa

revision = '0005_observability'
down_revision = '0004_upload_history'
branch_labels = None
depends_on = None


def upgrade():
    # events table for lightweight observability
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
          id BIGSERIAL PRIMARY KEY,
          ts TIMESTAMPTZ NOT NULL DEFAULT now(),
          component TEXT NOT NULL,
          duration_ms INTEGER,
          candidates INTEGER,
          citations INTEGER,
          insufficient BOOLEAN,
          payload JSONB
        );
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_events_component_ts
        ON events (component, ts DESC);
        """
    )

    # optional aggregated metrics storage (not required for runtime)
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS metrics_minute (
          ts TIMESTAMPTZ NOT NULL,
          window_sec INTEGER NOT NULL,
          p50_ms INTEGER,
          p95_ms INTEGER,
          rpm NUMERIC,
          error_rate_pct NUMERIC,
          count INTEGER,
          PRIMARY KEY (ts, window_sec)
        );
        """
    )


def downgrade():
    op.execute("DROP TABLE IF EXISTS metrics_minute;")
    op.execute("DROP INDEX IF EXISTS idx_events_component_ts;")
    op.execute("DROP TABLE IF EXISTS events;")


