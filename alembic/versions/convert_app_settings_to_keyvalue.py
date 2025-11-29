"""convert_app_settings_to_keyvalue

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2025-12-01 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - تبدیل به ساختار key-value"""
    # این migration فقط برای مستندات است
    # تبدیل واقعی با اسکریپت migrate_to_keyvalue.py انجام شده
    
    # بررسی اینکه آیا جدول به ساختار جدید تبدیل شده
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(app_settings)"))
    columns = {row[1]: row[2] for row in result.fetchall()}
    
    if 'setting_key' in columns:
        # قبلاً تبدیل شده
        return
    
    # اگر هنوز تبدیل نشده، باید تبدیل شود
    # این کار باید با اسکریپت migrate_to_keyvalue.py انجام شود
    # چون نیاز به تبدیل داده‌ها دارد
    pass


def downgrade() -> None:
    """Downgrade schema - تبدیل به ساختار قدیمی"""
    # تبدیل به ساختار قدیمی نیاز به migration داده‌ها دارد
    # این کار پیچیده است و بهتر است با اسکریپت جداگانه انجام شود
    pass

