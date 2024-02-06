"""empty message

Revision ID: 59388885a3fe
Revises: 365f4ca0a26b
Create Date: 2023-02-26 15:05:52.002624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59388885a3fe'
down_revision = '365f4ca0a26b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_profiles', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###
