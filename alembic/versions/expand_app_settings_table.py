"""expand_app_settings_table

Revision ID: a1b2c3d4e5f6
Revises: 3bc42188103b
Create Date: 2025-12-01 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '3bc42188103b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Helper function to check if column exists
    def column_exists(table_name, column_name):
        conn = op.get_bind()
        # SQLite PRAGMA - table_name is safe as it's hardcoded to 'app_settings'
        query = sa.text(f"PRAGMA table_info({table_name})")
        result = conn.execute(query)
        columns = [row[1] for row in result.fetchall()]
        return column_name in columns
    
    # Add new columns to app_settings table
    if not column_exists('app_settings', 'theme'):
        op.add_column('app_settings', sa.Column('theme', sa.String(length=20), nullable=True))
        # Set default value for existing rows
        op.execute("UPDATE app_settings SET theme = 'روشن' WHERE theme IS NULL")
    
    if not column_exists('app_settings', 'language'):
        op.add_column('app_settings', sa.Column('language', sa.String(length=50), nullable=True))
        op.execute("UPDATE app_settings SET language = 'فارسی' WHERE language IS NULL")
    
    if not column_exists('app_settings', 'notifications_enabled'):
        op.add_column('app_settings', sa.Column('notifications_enabled', sa.Boolean(), nullable=True))
        op.execute("UPDATE app_settings SET notifications_enabled = 1 WHERE notifications_enabled IS NULL")
    
    if not column_exists('app_settings', 'task_reminders'):
        op.add_column('app_settings', sa.Column('task_reminders', sa.Boolean(), nullable=True))
        op.execute("UPDATE app_settings SET task_reminders = 1 WHERE task_reminders IS NULL")
    
    if not column_exists('app_settings', 'auto_save'):
        op.add_column('app_settings', sa.Column('auto_save', sa.Boolean(), nullable=True))
        op.execute("UPDATE app_settings SET auto_save = 1 WHERE auto_save IS NULL")
    
    if not column_exists('app_settings', 'show_clock'):
        op.add_column('app_settings', sa.Column('show_clock', sa.Boolean(), nullable=True))
        op.execute("UPDATE app_settings SET show_clock = 1 WHERE show_clock IS NULL")
    
    if not column_exists('app_settings', 'show_status'):
        op.add_column('app_settings', sa.Column('show_status', sa.Boolean(), nullable=True))
        op.execute("UPDATE app_settings SET show_status = 1 WHERE show_status IS NULL")
    
    if not column_exists('app_settings', 'advanced_settings'):
        op.add_column('app_settings', sa.Column('advanced_settings', sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove added columns
    op.drop_column('app_settings', 'advanced_settings')
    op.drop_column('app_settings', 'show_status')
    op.drop_column('app_settings', 'show_clock')
    op.drop_column('app_settings', 'auto_save')
    op.drop_column('app_settings', 'task_reminders')
    op.drop_column('app_settings', 'notifications_enabled')
    op.drop_column('app_settings', 'language')
    op.drop_column('app_settings', 'theme')

