"""Add due_date index for performance

Revision ID: 002
Revises: 001
Create Date: 2026-01-09 14:00:00.000000

Per FR-034 and T110: Add index on due_date column for efficient sorting.
"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add index on tasks.due_date for efficient sorting per FR-034."""
    op.create_index(
        op.f('ix_tasks_due_date'),
        'tasks',
        ['due_date'],
        unique=False
    )


def downgrade() -> None:
    """Remove due_date index."""
    op.drop_index(op.f('ix_tasks_due_date'), table_name='tasks')
