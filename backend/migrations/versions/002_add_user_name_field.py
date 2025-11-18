"""Add name field to user model

Revision ID: 002_add_user_name_field
Revises: 001_initial_schema
Create Date: 2025-11-18

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002_add_user_name_field'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add name column to users table
    op.add_column('users', sa.Column('name', sa.String(length=100), nullable=True))


def downgrade() -> None:
    # Remove name column from users table
    op.drop_column('users', 'name')
