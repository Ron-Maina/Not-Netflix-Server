"""Updated password field

Revision ID: 59f2f5bc258b
Revises: 66ffae0dc337
Create Date: 2023-12-07 13:01:23.816779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59f2f5bc258b'
down_revision = '66ffae0dc337'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('_password_hash',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('_password_hash',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
