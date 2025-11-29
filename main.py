
import sys
from views.main_frameless_window import MainFramelessWindow
from PyQt6.QtWidgets import QApplication,QWidget

from configg.config_pages import ConfigPages
from services.db_session import init_db

# بهینه‌سازی: بارگذاری و اعمال استایل دارک
from utils.stylesheet_loader import load_stylesheet
from utils.app_config import AppConfig
from views.pages.first_run_settings_page import FirstRunSettingsDialog

app = QApplication(sys.argv)

# اعمال حالت دارک
dark_stylesheet = load_stylesheet("styles/dark.qss")
app.setStyleSheet(dark_stylesheet)

# Ensure all SQLAlchemy tables are created based on current models
init_db()

# انتقال داده‌های JSON قدیمی به دیتابیس (در صورت وجود)
from services.app_settings_service import AppSettingsService
AppSettingsService.migrate_from_json()

# بررسی اولین اجرا و نمایش صفحه تنظیمات
if AppConfig.is_first_run() or not AppConfig.is_setup_complete():
    settings_dialog = FirstRunSettingsDialog()
    settings_dialog.exec()
    # اگر کاربر دیالوگ را بست بدون تایید، برنامه را ببند
    if not AppConfig.is_setup_complete():
        sys.exit(0)

config = ConfigPages()


config.window.switch_page("Dashboard")
config.window.show()



sys.exit(app.exec())



