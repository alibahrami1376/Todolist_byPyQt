
import sys
from views.main_frameless_window import MainFramelessWindow
from PyQt6.QtWidgets import QApplication,QWidget

from configg.config_pages import ConfigPages


app = QApplication(sys.argv)

config = ConfigPages()


config.window.switch_page("Dashboard")
config.window.show()



sys.exit(app.exec())



