"""
مدیریت تنظیمات اولیه برنامه - استفاده از دیتابیس (ساختار key-value)
"""
from typing import Optional, Dict, Any
from services.app_settings_service import AppSettingsService


class AppConfig:
    """مدیریت تنظیمات برنامه - استفاده از دیتابیس (ساختار key-value)"""
    
    @staticmethod
    def is_first_run() -> bool:
        """بررسی اینکه آیا این اولین اجرای برنامه است"""
        return AppSettingsService.is_first_run()
    
    @staticmethod
    def get_config() -> Dict[str, Any]:
        """دریافت تمام تنظیمات ذخیره شده"""
        all_settings = AppSettingsService.get_all_settings()
        
        # ساختار قدیمی برای سازگاری
        return {
            'datetime': {
                'date': all_settings.get('date'),
                'time': all_settings.get('time'),
                'timezone': all_settings.get('timezone')
            },
            'theme': all_settings.get('theme', 'روشن'),
            'language': all_settings.get('language', 'فارسی'),
            'notifications': {
                'enabled': all_settings.get('notifications_enabled', True),
                'task_reminders': all_settings.get('task_reminders', True)
            },
            'general': {
                'auto_save': all_settings.get('auto_save', True),
                'show_clock': all_settings.get('show_clock', True),
                'show_status': all_settings.get('show_status', True)
            },
            'setup_completed': all_settings.get('setup_completed', False),
            'setup_date': all_settings.get('setup_date')
        }
    
    @staticmethod
    def save_config(config: Dict[str, Any]) -> None:
        """ذخیره تنظیمات"""
        # استخراج تنظیمات از ساختار config
        datetime_config = config.get('datetime', {})
        notifications_config = config.get('notifications', {})
        general_config = config.get('general', {})
        
        if datetime_config.get('date') and datetime_config.get('time'):
            AppSettingsService.save_datetime_settings(
                date=datetime_config.get('date'),
                time=datetime_config.get('time'),
                timezone=datetime_config.get('timezone')
            )
        
        if config.get('theme'):
            AppSettingsService.save_theme(config.get('theme'))
        
        if config.get('language'):
            AppSettingsService.save_language(config.get('language'))
        
        if notifications_config:
            AppSettingsService.save_notification_settings(
                notifications_enabled=notifications_config.get('enabled', True),
                task_reminders=notifications_config.get('task_reminders', True)
            )
        
        if general_config:
            AppSettingsService.set_setting('auto_save', general_config.get('auto_save', True))
            AppSettingsService.set_setting('show_clock', general_config.get('show_clock', True))
            AppSettingsService.set_setting('show_status', general_config.get('show_status', True))
        
        if config.get('setup_completed'):
            AppSettingsService.mark_setup_complete()
    
    @staticmethod
    def mark_setup_complete() -> None:
        """علامت‌گذاری که تنظیمات اولیه انجام شده"""
        AppSettingsService.mark_setup_complete()
    
    @staticmethod
    def is_setup_complete() -> bool:
        """بررسی اینکه آیا تنظیمات اولیه انجام شده"""
        return AppSettingsService.is_setup_complete()
    
    @staticmethod
    def save_datetime_settings(date: str, time: str, timezone: Optional[str] = None) -> None:
        """ذخیره تنظیمات تاریخ و زمان"""
        AppSettingsService.save_datetime_settings(date, time, timezone)
    
    @staticmethod
    def get_datetime_settings() -> Optional[Dict[str, str]]:
        """دریافت تنظیمات تاریخ و زمان"""
        return AppSettingsService.get_datetime_settings()
    
    @staticmethod
    def save_theme(theme: str) -> None:
        """ذخیره تنظیمات تم"""
        AppSettingsService.save_theme(theme)
    
    @staticmethod
    def get_theme() -> str:
        """دریافت تنظیمات تم"""
        return AppSettingsService.get_theme()
    
    @staticmethod
    def save_language(language: str) -> None:
        """ذخیره تنظیمات زبان"""
        AppSettingsService.save_language(language)
    
    @staticmethod
    def get_language() -> str:
        """دریافت تنظیمات زبان"""
        return AppSettingsService.get_language()
    
    @staticmethod
    def save_notification_settings(notifications_enabled: bool, task_reminders: bool) -> None:
        """ذخیره تنظیمات اعلان‌ها"""
        AppSettingsService.save_notification_settings(notifications_enabled, task_reminders)
    
    @staticmethod
    def get_notification_settings() -> Dict[str, bool]:
        """دریافت تنظیمات اعلان‌ها"""
        return AppSettingsService.get_notification_settings()
