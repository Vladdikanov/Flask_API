"""Initial migration2

Revision ID: 8a46cdf934f1
Revises: b97977d331b4
Create Date: 2025-03-22 06:31:11.908841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a46cdf934f1'
down_revision = 'b97977d331b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sale', schema=None) as batch_op:
        batch_op.add_column(sa.Column('discount', sa.Numeric(precision=100, scale=2), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sale', schema=None) as batch_op:
        batch_op.drop_column('discount')

    # ### end Alembic commands ###
