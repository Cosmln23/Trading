from alembic import op
import sqlalchemy as sa

revision = '0008_chat_tables'
down_revision = '0007_add_kind_to_upload_history'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'chat_sessions',
        sa.Column('id', sa.String(length=64), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_chat_sessions_expires', 'chat_sessions', ['expires_at'], unique=False)

    op.create_table(
        'chat_messages',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('chat_id', sa.String(length=64), sa.ForeignKey('chat_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('ts', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('role', sa.String(length=16), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('citations', sa.Integer, nullable=True),
    )
    op.create_index('ix_chat_messages_chat_id_ts', 'chat_messages', ['chat_id', 'ts'], unique=False)


def downgrade():
    op.drop_table('chat_messages')
    op.drop_table('chat_sessions')


