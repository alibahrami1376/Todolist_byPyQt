"""create_habits_tables

Revision ID: e54bbdb30bbb
Revises: 43f9165a3c39
Create Date: 2025-11-28 00:16:50.955751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e54bbdb30bbb'
down_revision: Union[str, None] = '43f9165a3c39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Helper function to check if table exists
    def table_exists(table_name):
        conn = op.get_bind()
        result = conn.execute(sa.text(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=:name"
        ), {"name": table_name})
        return result.fetchone() is not None
    
    # Create habits table if it doesn't exist
    if not table_exists('habits'):
        op.create_table('habits',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('goal_type', sa.String(length=20), nullable=False, server_default='boolean'),
    sa.Column('daily_goal', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
        )
    
    # Create habit_logs table if it doesn't exist
    if not table_exists('habit_logs'):
        op.create_table('habit_logs',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('habit_id', sa.String(length=50), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=False, server_default='1'),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['habit_id'], ['habits.id'], ),
    sa.PrimaryKeyConstraint('id')
        )
    
    # Create habit_stats table if it doesn't exist
    if not table_exists('habit_stats'):
        op.create_table('habit_stats',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('habit_id', sa.String(length=50), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('month', sa.Integer(), nullable=True),
    sa.Column('week', sa.Integer(), nullable=True),
    sa.Column('total_value', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('percent_success', sa.Float(), nullable=True, server_default='0.0'),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['habit_id'], ['habits.id'], ),
    sa.PrimaryKeyConstraint('id')
        )
    
    # Note: SQLite doesn't support ALTER COLUMN operations
    # The detected changes in existing tables are ignored for SQLite compatibility


def downgrade() -> None:
    """Downgrade schema."""
    # Drop habit tables in reverse order (due to foreign keys)
    op.drop_table('habit_stats')
    op.drop_table('habit_logs')
    op.drop_table('habits')
