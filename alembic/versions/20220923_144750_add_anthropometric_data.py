"""add anthropometric data

Revision ID: 4f9ff4b871da
Revises: c8b043de3c2d
Create Date: 2022-09-23 14:47:50.172024

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "4f9ff4b871da"
down_revision = "c8b043de3c2d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "anthropometric_data",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("weight", sa.Float(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("waist_circumference", sa.Integer(), nullable=True),
        sa.Column("fat_mass", sa.Float(), nullable=True),
        sa.Column("muscle_mass", sa.Float(), nullable=True),
        sa.Column("bone_mass", sa.Float(), nullable=True),
        sa.Column("body_water", sa.Float(), nullable=True),
        sa.Column("basal_metabolism", sa.Integer(), nullable=True),
        sa.Column("visceral_fat", sa.Integer(), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("anthropometric_data")
    # ### end Alembic commands ###
