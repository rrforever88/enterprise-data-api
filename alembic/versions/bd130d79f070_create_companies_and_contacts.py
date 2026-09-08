"""create companies and contacts

Revision ID: bd130d79f070
Revises: 
Create Date: 2026-09-08 14:01:48.429351

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd130d79f070'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.Column("industry", sa.String(length=100), nullable=False),
    )

    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False, unique=True),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("contacts")
    op.drop_table("companies")
