"""Fix Food Category relations

Revision ID: 14b5800edf0a
Revises: 9813c2511192
Create Date: 2022-06-17 17:51:35.443304

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '14b5800edf0a'
down_revision = '9813c2511192'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('food_category', sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.drop_constraint('food_category_parent_fkey', 'food_category', type_='foreignkey')
    op.create_foreign_key(None, 'food_category', 'food_category', ['parent_id'], ['id'])
    op.drop_column('food_category', 'parent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('food_category', sa.Column('parent', postgresql.UUID(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'food_category', type_='foreignkey')
    op.create_foreign_key('food_category_parent_fkey', 'food_category', 'food_category', ['parent'], ['id'])
    op.drop_column('food_category', 'parent_id')
    # ### end Alembic commands ###
