"""add item name

Revision ID: bad4f2a508fb
Revises: ccfd3fdb4ad3
Create Date: 2020-09-22 09:17:39.939801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bad4f2a508fb'
down_revision = 'ccfd3fdb4ad3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('name', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'name')
    # ### end Alembic commands ###
