from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0004_upload_history'
down_revision = '0003_embedding_vec_pgvector'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'upload_history',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('file_name', sa.String(length=256), nullable=False),
        sa.Column('file_size', sa.Integer, nullable=True),
        sa.Column('file_hash', sa.String(length=64), nullable=True),
        sa.Column('doc_id', sa.String(length=128), nullable=True),
        sa.Column('collection', sa.String(length=64), nullable=True),
        sa.Column('text_chars', sa.Integer, nullable=True),
        sa.Column('chunk_count', sa.Integer, nullable=True),
        sa.Column('inserted_count', sa.Integer, nullable=True),
        sa.Column('skipped_conflict_count', sa.Integer, nullable=True),
        sa.Column('embedded_count', sa.Integer, nullable=True),
        sa.Column('ocr_used', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('upload_history')


