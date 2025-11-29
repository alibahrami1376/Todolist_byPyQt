"""create_courses_textbooks_learning_loops_tables

Revision ID: f7g8h9i0j1k2
Revises: e54bbdb30bbb
Create Date: 2025-11-29 14:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7g8h9i0j1k2'
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
    
    # Create courses table if it doesn't exist
    if not table_exists('courses'):
        op.create_table('courses',
            sa.Column('id', sa.String(length=50), nullable=False),
            sa.Column('title', sa.String(length=200), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('start_date', sa.Date(), nullable=True),
            sa.Column('link', sa.String(length=500), nullable=True),
            sa.Column('status', sa.String(length=50), nullable=False, server_default='در حال انجام'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
    
    # Create textbooks table if it doesn't exist
    if not table_exists('textbooks'):
        op.create_table('textbooks',
            sa.Column('id', sa.String(length=50), nullable=False),
            sa.Column('title', sa.String(length=200), nullable=False),
            sa.Column('content', sa.Text(), nullable=True),
            sa.Column('course_id', sa.String(length=50), nullable=True),
            sa.Column('link', sa.String(length=500), nullable=True),
            sa.Column('progress', sa.Float(), nullable=False, server_default='0.0'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
    
    # Create learning_loops table if it doesn't exist
    if not table_exists('learning_loops'):
        op.create_table('learning_loops',
            sa.Column('id', sa.String(length=50), nullable=False),
            sa.Column('textbook_id', sa.String(length=50), nullable=False),
            sa.Column('title', sa.String(length=200), nullable=False),
            sa.Column('content', sa.Text(), nullable=True),
            sa.Column('completed', sa.Boolean(), nullable=False, server_default='0'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['textbook_id'], ['textbooks.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
    
    # Create documents table if it doesn't exist
    if not table_exists('documents'):
        op.create_table('documents',
            sa.Column('id', sa.String(length=50), nullable=False),
            sa.Column('title', sa.String(length=200), nullable=False),
            sa.Column('course_id', sa.String(length=50), nullable=True),
            sa.Column('textbook_id', sa.String(length=50), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
            sa.ForeignKeyConstraint(['textbook_id'], ['textbooks.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
    
    # Create document_blocks table if it doesn't exist
    if not table_exists('document_blocks'):
        op.create_table('document_blocks',
            sa.Column('id', sa.String(length=50), nullable=False),
            sa.Column('document_id', sa.String(length=50), nullable=False),
            sa.Column('block_type', sa.String(length=50), nullable=False),
            sa.Column('content', sa.Text(), nullable=True),
            sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('block_metadata', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop tables in reverse order (due to foreign keys)
    op.drop_table('document_blocks')
    op.drop_table('documents')
    op.drop_table('learning_loops')
    op.drop_table('textbooks')
    op.drop_table('courses')

