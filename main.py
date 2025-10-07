
import sys
from views.main_frameless_window import MainFramelessWindow
from PyQt6.QtWidgets import QApplication,QWidget

from configg.config_pages import ConfigPages
from services.db_session import init_db

# بهینه‌سازی: بارگذاری و اعمال استایل دارک
from utils.stylesheet_loader import load_stylesheet


app = QApplication(sys.argv)

# اعمال حالت دارک
dark_stylesheet = load_stylesheet("styles/dark.qss")
app.setStyleSheet(dark_stylesheet)

# Ensure all SQLAlchemy tables are created based on current models
init_db()

config = ConfigPages()


config.window.switch_page("Dashboard")
config.window.show()



sys.exit(app.exec())



