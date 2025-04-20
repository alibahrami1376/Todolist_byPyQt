
import sys
from views.main_frameless_window import MainFramelessWindow
from PyQt6.QtWidgets import QApplication

from views.pages.dashboard_page import DashboardPage
from views.pages.calendar_page import CalendarPage
from views.pages.settings_pages import SettingsPage

from views.pages.login_page import LoginPage
from views.pages.about_page import AboutPage
from views.pages.journal_page import JournalPage
from views.pages.timer_page import TimerPage
from views.pages.todolist_page import TodoListPage

app = QApplication(sys.argv)
window = MainFramelessWindow()


login_page = LoginPage()

window.add_page(DashboardPage(),"Dashboard")
window.add_page(CalendarPage(),"Calendar")
window.add_page(SettingsPage(), "Settings")
window.add_page(login_page, "Login")
window.add_page(AboutPage(), "About")
window.add_page(JournalPage(), "Journal")
window.add_page(TimerPage(), "Timer")
window.add_page(TodoListPage(), "TodoList")


# # اتصال سیگنال login
# login_page.login_requested.connect(handle_login)

# # اتصال سیگنال register
# login_page.register_requested.connect(lambda: window.switch_page("register"))

# # اتصال سیگنال guest
# login_page.guest_requested.connect(lambda: window.switch_page("home"))






window.switch_page("Dashboard")
window.show()


sys.exit(app.exec())



