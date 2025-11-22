"""add_description_category_tags_priority_score_to_ideas

Revision ID: 43f9165a3c39
Revises: 6cb37620cac9
Create Date: 2025-11-22 17:42:09.465782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43f9165a3c39'
down_revision: Union[str, None] = '6cb37620cac9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite doesn't support ALTER COLUMN for type/nullable changes
    # Only adding new columns which SQLite supports
    
    # Helper function to check if column exists
    def column_exists(table_name, column_name):
        conn = op.get_bind()
        # PRAGMA doesn't support parameters, but table_name is from our code, so it's safe
        result = conn.execute(sa.text(f"PRAGMA table_info({table_name})"))
        columns = [row[1] for row in result.fetchall()]
        return column_name in columns
    
    # Add columns to ideas table if they don't exist
    if not column_exists('ideas', 'description'):
        op.add_column('ideas', sa.Column('description', sa.Text(), nullable=True))
    if not column_exists('ideas', 'category'):
        op.add_column('ideas', sa.Column('category', sa.String(length=100), nullable=True))
    if not column_exists('ideas', 'tags'):
        op.add_column('ideas', sa.Column('tags', sa.String(length=300), nullable=True))
    if not column_exists('ideas', 'priority'):
        op.add_column('ideas', sa.Column('priority', sa.String(length=20), nullable=True))
    op.execute(sa.text("UPDATE ideas SET priority = 'medium' WHERE priority IS NULL"))
    
    if not column_exists('ideas', 'score'):
        op.add_column('ideas', sa.Column('score', sa.Integer(), nullable=True))
    op.execute(sa.text("UPDATE ideas SET score = 0 WHERE score IS NULL"))
    
    # Add columns to project_steps table if they don't exist
    if not column_exists('project_steps', 'description'):
        op.add_column('project_steps', sa.Column('description', sa.Text(), nullable=True))
    if not column_exists('project_steps', 'order'):
        op.add_column('project_steps', sa.Column('order', sa.Integer(), nullable=True))
    op.execute(sa.text("UPDATE project_steps SET [order] = 0 WHERE [order] IS NULL"))
    
    # Add columns to projects table if they don't exist
    if not column_exists('projects', 'description'):
        op.add_column('projects', sa.Column('description', sa.Text(), nullable=True))
    if not column_exists('projects', 'tech_stack'):
        op.add_column('projects', sa.Column('tech_stack', sa.String(length=300), nullable=True))
    if not column_exists('projects', 'progress'):
        op.add_column('projects', sa.Column('progress', sa.Integer(), nullable=True))
    op.execute(sa.text("UPDATE projects SET progress = 0 WHERE progress IS NULL"))
    
    # Note: Type changes and nullable changes are skipped for SQLite compatibility
    # SQLite doesn't enforce VARCHAR lengths or strict nullability anyway


def downgrade() -> None:
    """Downgrade schema."""
    # Drop added columns
    op.drop_column('projects', 'progress')
    op.drop_column('projects', 'tech_stack')
    op.drop_column('projects', 'description')
    op.drop_column('project_steps', 'order')
    op.drop_column('project_steps', 'description')
    op.drop_column('ideas', 'score')
    op.drop_column('ideas', 'priority')
    op.drop_column('ideas', 'tags')
    op.drop_column('ideas', 'category')
    op.drop_column('ideas', 'description')
