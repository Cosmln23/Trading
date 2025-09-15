from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        'fragments',
        sa.Column('id', sa.String(length=128), primary_key=True),
        sa.Column('doc_id', sa.String(length=128), nullable=False),
        sa.Column('collection', sa.String(length=64), nullable=False),
        sa.Column('page', sa.Integer, nullable=True),
        sa.Column('chunk_index', sa.Integer, nullable=True),
        sa.Column('text', sa.Text, nullable=False),
        sa.Column('embedding', sa.dialects.postgresql.ARRAY(sa.Float), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'journal',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('timestamp', sa.String(length=32), nullable=False),
        sa.Column('strategy', sa.String(length=1), nullable=False),
        sa.Column('symbol', sa.String(length=32), nullable=True),
        sa.Column('direction', sa.String(length=8), nullable=True),
        sa.Column('entry', sa.Float, nullable=True),
        sa.Column('size', sa.Float, nullable=True),
        sa.Column('stop', sa.Float, nullable=True),
        sa.Column('tp', sa.Float, nullable=True),
        sa.Column('rationale', sa.Text, nullable=True),
        sa.Column('tags', sa.Text, nullable=True),
        sa.Column('status', sa.String(length=8), nullable=True),
        sa.Column('rr', sa.Float, nullable=True),
        sa.Column('pnl', sa.Float, nullable=True),
        sa.Column('answer_id', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'events',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('time', sa.String(length=16), nullable=True),
        sa.Column('type', sa.String(length=16), nullable=True),
        sa.Column('symbol', sa.String(length=32), nullable=True),
        sa.Column('title', sa.String(length=256), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('events')
    op.drop_table('journal')
    op.drop_table('fragments')
