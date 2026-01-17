"""add_name_field_to_users

Revision ID: 169007143fd3
Revises: 002
Create Date: 2026-01-16 10:18:29.776407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '169007143fd3'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add name column to users table
    # Using server_default for existing rows, will remove after data migration
    op.add_column(
        'users',
        sa.Column('name', sa.String(length=100), nullable=False, server_default='Unknown User')
    )

    # Remove server_default after adding column (only needed for existing rows)
    op.alter_column('users', 'name', server_default=None)


def downgrade() -> None:
    # Remove name column from users table
    op.drop_column('users', 'name')
