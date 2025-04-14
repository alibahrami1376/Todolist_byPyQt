import sys
from PyQt6.QtWidgets import QApplication
from views.view_home import TaskManagerWindow
from views.view_pagemanager import PageManagerWindow
from views.view_login import LoginPage
from viewmodels.task_view_models import TaskViewModel

from utils.stylesheet_loader import load_stylesheet

app = QApplication(sys.argv)
app.setStyleSheet(load_stylesheet("styles/dark.qss"))

manager = PageManagerWindow()

# ساخت نمونه صفحات
home_page = TaskManagerWindow(manager, TaskViewModel())
Login_page = LoginPage(manager)

# اضافه کردن صفحات به manager
manager.add_page(home_page, "home")
manager.add_page(Login_page, "login")

# صفحه پیش فرض
manager.switch_page("login")
# نمایش manager
manager.setWindowTitle("Todo List")
manager.show()

sys.exit(app.exec())