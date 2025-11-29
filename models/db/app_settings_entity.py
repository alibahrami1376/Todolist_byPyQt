"""
Entity برای ذخیره تنظیمات اولیه برنامه
ساختار key-value: هر تنظیمات در یک ردیف جداگانه
"""
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from services.db_session import Base


class AppSettingsEntity(Base):
    """جدول تنظیمات برنامه - ساختار key-value"""
    __tablename__ = "app_settings"
    
    __table_args__ = (
        UniqueConstraint('setting_key', name='uq_app_settings_key'),
    )

    id: Mapped[str] = mapped_column(
        String(50), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4().hex)
    )
    
    # کلید تنظیمات (مثلاً: 'theme', 'language', 'date', 'time', ...)
    setting_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    # مقدار تنظیمات (به صورت string ذخیره می‌شود)
    setting_value: Mapped[str] = mapped_column(Text, nullable=True)
    
    # نوع داده (برای تبدیل صحیح: 'string', 'boolean', 'integer', 'json')
    value_type: Mapped[str] = mapped_column(String(20), nullable=False, default='string')
    
    # توضیحات (اختیاری)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # تاریخ ایجاد و به‌روزرسانی
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.utcnow()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow()
    )

