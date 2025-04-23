# page_registry.py

from views.pages.login_page import LoginPage
from views.pages.about_page import AboutPage
from views.pages.journal_page import JournalPage
from views.pages.timer_page import TimerPage
from views.pages.todolist_page import TodoListPage
from views.pages.userdashboard_page import UserDashboardPage
from views.pages.dashboard_page import DashboardPage
from views.pages.calendar_page import CalendarPage
from views.pages.settings_pages import SettingsPage
from views.pages.register_page import RegisterPage

class PageRegistry:
    def __init__(self):
        self.dash = DashboardPage()
        self.calendar = CalendarPage()
        self.settings = SettingsPage()
        self.login = LoginPage()
        self.about = AboutPage()
        self.journal = JournalPage()
        self.timer = TimerPage()
        self.todo = TodoListPage()
        self.userdash = UserDashboardPage()
        self.register = RegisterPage()
