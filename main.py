import sys
from PyQt6.QtWidgets import QApplication
from views.view_home import TaskManagerWindow
from views.view_pagemanager import PageManagerWindow
from views.view_login import LoginPage

app = QApplication(sys.argv)

manager = PageManagerWindow()

# ساخت نمونه صفحات
home_page = TaskManagerWindow(manager)
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