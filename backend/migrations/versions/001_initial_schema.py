"""Initial database schema

Revision ID: 001_initial_schema
Revises:
Create Date: 2025-11-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('language', sa.String(length=2), server_default='en', nullable=False),
        sa.Column('timezone', sa.String(length=50), server_default='UTC', nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.CheckConstraint("language IN ('en', 'pl')", name='check_language'),
        sa.CheckConstraint('email = LOWER(email)', name='check_email_lowercase')
    )
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_created_at', 'users', ['created_at'])

    # Create metrics table
    op.create_table(
        'metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name_key', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('value_type', sa.String(length=20), nullable=False),
        sa.Column('min_value', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('max_value', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('color', sa.String(length=7), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('display_order', sa.Integer(), server_default='0', nullable=True),
        sa.Column('archived', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'name_key', name='unique_user_metric_name'),
        sa.CheckConstraint(
            "category IN ('physical', 'psychological', 'triggers', 'medications', 'selfcare', 'wellness', 'notes')",
            name='check_category'
        ),
        sa.CheckConstraint(
            "value_type IN ('range', 'number', 'boolean', 'count', 'text')",
            name='check_value_type'
        ),
        sa.CheckConstraint(
            "(value_type != 'range') OR (min_value IS NOT NULL AND max_value IS NOT NULL AND min_value < max_value)",
            name='check_valid_range'
        )
    )
    op.create_index('idx_metrics_user_id', 'metrics', ['user_id'])
    op.create_index('idx_metrics_category', 'metrics', ['category'])
    op.create_index('idx_metrics_archived', 'metrics', ['archived'])

    # Create entries table
    op.create_table(
        'entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('entry_date', sa.Date(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'entry_date', name='unique_user_date'),
        sa.CheckConstraint('entry_date <= CURRENT_DATE', name='check_entry_date_not_future')
    )
    op.create_index('idx_entries_user_id', 'entries', ['user_id'])
    op.create_index('idx_entries_date', 'entries', ['entry_date'])
    op.create_index('idx_entries_user_date', 'entries', ['user_id', 'entry_date'])

    # Create entry_values table
    op.create_table(
        'entry_values',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entry_id', sa.Integer(), nullable=False),
        sa.Column('metric_id', sa.Integer(), nullable=False),
        sa.Column('value_numeric', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('value_boolean', sa.Boolean(), nullable=True),
        sa.Column('value_text', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['entry_id'], ['entries.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['metric_id'], ['metrics.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('entry_id', 'metric_id', name='unique_entry_metric'),
        sa.CheckConstraint(
            '(value_numeric IS NOT NULL) OR (value_boolean IS NOT NULL) OR (value_text IS NOT NULL)',
            name='check_value_not_null'
        )
    )
    op.create_index('idx_entry_values_entry_id', 'entry_values', ['entry_id'])
    op.create_index('idx_entry_values_metric_id', 'entry_values', ['metric_id'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index('idx_entry_values_metric_id', table_name='entry_values')
    op.drop_index('idx_entry_values_entry_id', table_name='entry_values')
    op.drop_table('entry_values')

    op.drop_index('idx_entries_user_date', table_name='entries')
    op.drop_index('idx_entries_date', table_name='entries')
    op.drop_index('idx_entries_user_id', table_name='entries')
    op.drop_table('entries')

    op.drop_index('idx_metrics_archived', table_name='metrics')
    op.drop_index('idx_metrics_category', table_name='metrics')
    op.drop_index('idx_metrics_user_id', table_name='metrics')
    op.drop_table('metrics')

    op.drop_index('idx_users_created_at', table_name='users')
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')
