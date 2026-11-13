"""add personas

Revision ID: 0003_personas
Revises: 0002_lessons_tests
Create Date: 2026-11-11 16:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0003_personas"
down_revision = "0002_lessons_tests"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "personas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=255), nullable=False),
        sa.Column("region", sa.String(length=100), nullable=False),
        sa.Column("niche", sa.String(length=100), nullable=False),
        sa.Column("difficulty", sa.String(length=50), nullable=False, server_default="medium"),
        sa.Column("temperament", sa.String(length=100), nullable=True),
        sa.Column("budget_level", sa.String(length=50), nullable=True),
        sa.Column("urgency_level", sa.String(length=50), nullable=True),
        sa.Column("hidden_pain", sa.Text(), nullable=True),
        sa.Column("objections", sa.Text(), nullable=True),
        sa.Column("buy_conditions", sa.Text(), nullable=True),
        sa.Column("fail_conditions", sa.Text(), nullable=True),
        sa.Column("tags", sa.Text(), nullable=True),
        sa.Column("system_prompt", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_personas_code"), "personas", ["code"], unique=True)
    op.create_index(op.f("ix_personas_id"), "personas", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_personas_id"), table_name="personas")
    op.drop_index(op.f("ix_personas_code"), table_name="personas")
    op.drop_table("personas")