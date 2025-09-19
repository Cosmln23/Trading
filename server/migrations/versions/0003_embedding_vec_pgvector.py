from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003_embedding_vec_pgvector'
down_revision = '0002_chunk_hash_dedup'
branch_labels = None
depends_on = None


def upgrade():
    # Ensure extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    # Add embedding_vec column if missing
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_name='fragments' AND column_name='embedding_vec'
        ) THEN
            ALTER TABLE fragments ADD COLUMN embedding_vec vector(768);
        END IF;
    END$$;
    """)
    # Optional: create IVFFLAT index if not exists (requires populated data)
    op.execute("CREATE INDEX IF NOT EXISTS idx_fragments_vec ON fragments USING ivfflat (embedding_vec);")


def downgrade():
    op.execute("DROP INDEX IF EXISTS idx_fragments_vec;")
    op.execute("""
    ALTER TABLE fragments DROP COLUMN IF EXISTS embedding_vec;
    """)



