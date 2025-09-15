from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_chunk_hash_dedup'
down_revision = '0001_init'
branch_labels = None
depends_on = None


def upgrade():
    # Add chunk_hash column for deduplication
    op.add_column('fragments', sa.Column('chunk_hash', sa.String(length=64), nullable=True))
    # Backfill chunk_hash using md5(text)
    op.execute("UPDATE fragments SET chunk_hash = md5(text) WHERE chunk_hash IS NULL")
    # Unique constraint to ensure doc_id + chunk_hash is unique
    op.create_unique_constraint('uq_fragments_docid_chunkhash', 'fragments', ['doc_id', 'chunk_hash'])


def downgrade():
    op.drop_constraint('uq_fragments_docid_chunkhash', 'fragments', type_='unique')
    op.drop_column('fragments', 'chunk_hash')


