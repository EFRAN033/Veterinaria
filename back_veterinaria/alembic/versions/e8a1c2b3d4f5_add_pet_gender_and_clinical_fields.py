"""add pet gender and appointment clinical fields

Revision ID: e8a1c2b3d4f5
Revises: 72b7b3cc1c38
Create Date: 2026-04-20

"""
from alembic import op
import sqlalchemy as sa


revision = "e8a1c2b3d4f5"
down_revision = "72b7b3cc1c38"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("pets", sa.Column("gender", sa.String(length=20), nullable=True))
    op.add_column(
        "appointments",
        sa.Column("final_diagnosis", sa.Text(), nullable=True),
    )
    op.add_column("appointments", sa.Column("treatment", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("appointments", "treatment")
    op.drop_column("appointments", "final_diagnosis")
    op.drop_column("pets", "gender")
