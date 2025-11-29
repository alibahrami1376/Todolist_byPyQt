"""
Service برای مدیریت تنظیمات برنامه - ساختار key-value
"""
import json
import os
from typing import Optional, Dict, Any, List
from datetime import datetime
from services.db_session import get_session
from models.db.app_settings_entity import AppSettingsEntity


class AppSettingsService:
    """مدیریت تنظیمات برنامه در دیتابیس - ساختار key-value"""
    
    @staticmethod
    def _convert_value(value: Any, value_type: str) -> Any:
        """تبدیل مقدار string به نوع داده صحیح"""
        if value is None:
            return None
        
        if value_type == 'boolean':
            if isinstance(value, bool):
                return value
            return str(value).lower() in ('true', '1', 'yes', 'on')
        elif value_type == 'integer':
            try:
                return int(value)
            except (ValueError, TypeError):
                return 0
        elif value_type == 'json':
            try:
                return json.loads(value) if isinstance(value, str) else value
            except (json.JSONDecodeError, TypeError):
                return {}
        else:  # string
            return str(value)
    
    @staticmethod
    def _serialize_value(value: Any) -> tuple[str, str]:
        """تبدیل مقدار به string و تعیین نوع"""
        if isinstance(value, bool):
            return (str(value).lower(), 'boolean')
        elif isinstance(value, int):
            return (str(value), 'integer')
        elif isinstance(value, (dict, list)):
            return (json.dumps(value, ensure_ascii=False), 'json')
        else:
            return (str(value), 'string')
    
    @staticmethod
    def set_setting(key: str, value: Any, description: Optional[str] = None) -> AppSettingsEntity:
        """ذخیره یا به‌روزرسانی یک تنظیمات"""
        with get_session() as session:
            setting = session.query(AppSettingsEntity).filter(
                AppSettingsEntity.setting_key == key
            ).first()
            
            value_str, value_type = AppSettingsService._serialize_value(value)
            
            if setting is None:
                # ایجاد تنظیمات جدید
                setting = AppSettingsEntity(
                    setting_key=key,
                    setting_value=value_str,
                    value_type=value_type,
                    description=description
                )
                session.add(setting)
            else:
                # به‌روزرسانی تنظیمات موجود
                setting.setting_value = value_str
                setting.value_type = value_type
                if description is not None:
                    setting.description = description
                setting.updated_at = datetime.utcnow()
            
            session.commit()
            session.refresh(setting)
            return setting
    
    @staticmethod
    def get_setting(key: str, default: Any = None) -> Any:
        """دریافت یک تنظیمات"""
        with get_session() as session:
            setting = session.query(AppSettingsEntity).filter(
                AppSettingsEntity.setting_key == key
            ).first()
            
            if setting is None:
                return default
            
            return AppSettingsService._convert_value(setting.setting_value, setting.value_type)
    
    @staticmethod
    def delete_setting(key: str) -> bool:
        """حذف یک تنظیمات"""
        with get_session() as session:
            setting = session.query(AppSettingsEntity).filter(
                AppSettingsEntity.setting_key == key
            ).first()
            
            if setting:
                session.delete(setting)
                session.commit()
                return True
            return False
    
    @staticmethod
    def get_all_settings() -> Dict[str, Any]:
        """دریافت تمام تنظیمات به صورت دیکشنری"""
        with get_session() as session:
            settings = session.query(AppSettingsEntity).all()
            result = {}
            for setting in settings:
                result[setting.setting_key] = AppSettingsService._convert_value(
                    setting.setting_value, 
                    setting.value_type
                )
            return result
    
    @staticmethod
    def get_all_settings_entities() -> List[AppSettingsEntity]:
        """دریافت تمام تنظیمات به صورت لیست Entity"""
        with get_session() as session:
            return session.query(AppSettingsEntity).all()
    
    # متدهای کمکی برای تنظیمات خاص
    
    @staticmethod
    def save_theme(theme: str) -> None:
        """ذخیره تنظیمات تم"""
        AppSettingsService.set_setting('theme', theme, 'تم برنامه (روشن/دارک)')
    
    @staticmethod
    def get_theme() -> str:
        """دریافت تنظیمات تم"""
        return AppSettingsService.get_setting('theme', 'روشن')
    
    @staticmethod
    def save_language(language: str) -> None:
        """ذخیره تنظیمات زبان"""
        AppSettingsService.set_setting('language', language, 'زبان برنامه')
    
    @staticmethod
    def get_language() -> str:
        """دریافت تنظیمات زبان"""
        return AppSettingsService.get_setting('language', 'فارسی')
    
    @staticmethod
    def save_datetime_settings(date: str, time: str, timezone: Optional[str] = None) -> None:
        """ذخیره تنظیمات تاریخ و زمان"""
        AppSettingsService.set_setting('date', date, 'تاریخ')
        AppSettingsService.set_setting('time', time, 'زمان')
        if timezone:
            AppSettingsService.set_setting('timezone', timezone, 'منطقه زمانی')
    
    @staticmethod
    def get_datetime_settings() -> Optional[Dict[str, str]]:
        """دریافت تنظیمات تاریخ و زمان"""
        date = AppSettingsService.get_setting('date')
        time = AppSettingsService.get_setting('time')
        if date is None or time is None:
            return None
        return {
            'date': date,
            'time': time,
            'timezone': AppSettingsService.get_setting('timezone')
        }
    
    @staticmethod
    def save_notification_settings(notifications_enabled: bool, task_reminders: bool) -> None:
        """ذخیره تنظیمات اعلان‌ها"""
        AppSettingsService.set_setting('notifications_enabled', notifications_enabled, 'فعال بودن اعلان‌ها')
        AppSettingsService.set_setting('task_reminders', task_reminders, 'یادآوری تسک‌ها')
    
    @staticmethod
    def get_notification_settings() -> Dict[str, bool]:
        """دریافت تنظیمات اعلان‌ها"""
        return {
            'notifications_enabled': AppSettingsService.get_setting('notifications_enabled', True),
            'task_reminders': AppSettingsService.get_setting('task_reminders', True)
        }
    
    @staticmethod
    def is_setup_complete() -> bool:
        """بررسی اینکه آیا تنظیمات اولیه انجام شده"""
        return AppSettingsService.get_setting('setup_completed', False)
    
    @staticmethod
    def mark_setup_complete() -> None:
        """علامت‌گذاری که تنظیمات اولیه انجام شده"""
        AppSettingsService.set_setting('setup_completed', True, 'وضعیت تکمیل تنظیمات اولیه')
        AppSettingsService.set_setting('setup_date', datetime.utcnow().isoformat(), 'تاریخ تکمیل تنظیمات')
    
    @staticmethod
    def is_first_run() -> bool:
        """بررسی اینکه آیا این اولین اجرای برنامه است"""
        # اگر هیچ تنظیماتی وجود نداشته باشد، اولین اجرا است
        with get_session() as session:
            count = session.query(AppSettingsEntity).count()
            return count == 0
    
    @staticmethod
    def migrate_from_json() -> bool:
        """
        انتقال داده‌های JSON قدیمی و فایل‌های تنظیمات به دیتابیس (در صورت وجود)
        Returns: True if migration was performed, False otherwise
        """
        # بررسی وجود تنظیمات در دیتابیس
        if not AppSettingsService.is_first_run():
            return False  # قبلاً migration انجام شده
        
        migrated = False
        
        # 1. انتقال از فایل JSON قدیمی
        json_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'data', 
            'app_config.json'
        )
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # انتقال تنظیمات datetime
                datetime_config = config.get('datetime', {})
                if datetime_config.get('date') and datetime_config.get('time'):
                    AppSettingsService.save_datetime_settings(
                        date=datetime_config.get('date'),
                        time=datetime_config.get('time'),
                        timezone=datetime_config.get('timezone')
                    )
                
                # انتقال setup_completed
                if config.get('setup_completed'):
                    AppSettingsService.mark_setup_complete()
                
                # بکاپ گرفتن از فایل JSON
                backup_path = json_path + '.backup'
                if not os.path.exists(backup_path):
                    import shutil
                    shutil.copy2(json_path, backup_path)
                
                migrated = True
            except (json.JSONDecodeError, IOError, Exception):
                pass
        
        # 2. انتقال تنظیمات تم از فایل theme_config.txt
        theme_config_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'configg',
            'theme_config.txt'
        )
        
        if os.path.exists(theme_config_path):
            try:
                with open(theme_config_path, 'r', encoding='utf-8') as f:
                    theme = f.read().strip()
                    if theme in ["روشن", "دارک"]:
                        AppSettingsService.save_theme(theme)
                        migrated = True
            except (IOError, Exception):
                pass
        
        return migrated
