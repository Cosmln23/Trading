from alembic import op
import sqlalchemy as sa

revision = '0007_add_kind_to_upload_history'
down_revision = '0006_qa_tables'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('upload_history') as batch_op:
        batch_op.add_column(sa.Column('kind', sa.String(length=16), nullable=True))


def downgrade():
    with op.batch_alter_table('upload_history') as batch_op:
        batch_op.drop_column('kind')


