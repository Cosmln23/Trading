from alembic import op
import sqlalchemy as sa

revision = '0009_portfolio_tables'
down_revision = '0008_chat_tables'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'portfolio_snapshots',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('ts', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('note', sa.Text, nullable=True),
        sa.Column('source', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_portfolio_snapshots_ts', 'portfolio_snapshots', ['ts'], unique=False)

    op.create_table(
        'portfolio_holdings',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('snapshot_id', sa.BigInteger, sa.ForeignKey('portfolio_snapshots.id', ondelete='CASCADE'), nullable=False),
        sa.Column('symbol', sa.String(length=32), nullable=False),
        sa.Column('quantity', sa.Numeric, nullable=True),
        sa.Column('cost', sa.Numeric, nullable=True),
        sa.Column('tags', sa.Text, nullable=True),
    )
    op.create_index('ix_portfolio_holdings_snapshot', 'portfolio_holdings', ['snapshot_id'], unique=False)
    op.create_index('ix_portfolio_holdings_symbol', 'portfolio_holdings', ['symbol'], unique=False)


def downgrade():
    op.drop_table('portfolio_holdings')
    op.drop_table('portfolio_snapshots')


