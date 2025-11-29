"""create_app_settings_table

Revision ID: 3bc42188103b
Revises: e54bbdb30bbb
Create Date: 2025-11-28 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bc42188103b'
down_revision: Union[str, None] = 'e54bbdb30bbb'
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
    
    # Create app_settings table if it doesn't exist
    if not table_exists('app_settings'):
        op.create_table('app_settings',
            sa.Column('id', sa.String(length=50), nullable=False),
            sa.Column('date', sa.String(length=50), nullable=True),
            sa.Column('time', sa.String(length=50), nullable=True),
            sa.Column('timezone', sa.String(length=100), nullable=True),
            sa.Column('setup_completed', sa.Boolean(), nullable=False, server_default='0'),
            sa.Column('setup_date', sa.DateTime(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('app_settings')

