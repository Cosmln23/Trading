from alembic import op
import sqlalchemy as sa

revision = '0006_qa_tables'
down_revision = '0005_observability'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS qa_questions (
          id BIGSERIAL PRIMARY KEY,
          collection TEXT NOT NULL,
          question TEXT NOT NULL,
          expected_doc_ids TEXT[] NOT NULL
        );
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS qa_runs (
          id BIGSERIAL PRIMARY KEY,
          ts TIMESTAMPTZ NOT NULL DEFAULT now(),
          question_id BIGINT NOT NULL REFERENCES qa_questions(id) ON DELETE CASCADE,
          citations_doc_ids TEXT[] NOT NULL,
          precision5 NUMERIC,
          hallucination BOOLEAN
        );
        """
    )


def downgrade():
    op.execute("DROP TABLE IF EXISTS qa_runs;")
    op.execute("DROP TABLE IF EXISTS qa_questions;")


