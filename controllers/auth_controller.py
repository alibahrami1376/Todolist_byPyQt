

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject

from views.pages.login_page import LoginPage
from views.main_frameless_window import MainFramelessWindow
from viewmodels.auth_viewmodel import UserViewModel
from utils.app_notifier import AppNotifier

from core.session_manager import Session

from views.pages.register_page import RegisterPage
from views.pages.userdashboard_page import UserDashboardPage

class AuthController(QObject):
    def __init__(
        self,
        login_page: LoginPage,
        userdash_page: UserDashboardPage,
        register_page: RegisterPage,
        page_manager: MainFramelessWindow
        ):
        super().__init__()
        self.login_page= login_page
        self.userdash_page= userdash_page
        self.register_page= register_page
        self.page_manager = page_manager
        self.user_viewmodel = UserViewModel()
       

        self.connect_signals()

    def connect_signals(self):
        self.login_page.login_requested.connect(self.handle_login)
        self.login_page.register_requested.connect(self.handle_register)
        self.login_page.guest_requested.connect(self.continue_as_guest)
       
    def handle_login(self, username: str, password: str):
        user = self.user_viewmodel.validate_credentials(username,password)
        if user:
            Session.set_user(user)
            AppNotifier(QWidget).warning("Success","You have successfully logged in.")
           
            self.userdash_page.logout_requested.connect(self.handle_logout)
            self.page_manager.change_page(self.userdash_page,"Login")
        else:
           return AppNotifier(QWidget).warning("Login Failed","Incorrect username or password. Please try again.")

    def handle_register(self):
        register_dialog = self.register_page
        register_dialog.register_submitted.connect(self.event_register)
        register_dialog.exec()

        
    def event_register(self,data: dict):
        user = self.user_viewmodel.register_dict(data)


    def continue_as_guest(self):
        user = self.user_viewmodel.creat_guest()
        Session.set_user(user)
        AppNotifier(QWidget).warning("Success","You have successfully logged in.")
        self.userdash_page.logout_requested.connect(self.handle_logout)
        self.page_manager.change_page(self.userdash_page,"Login")


    def handle_logout(self):
        Session.clear_user_current()
        self.page_manager.change_page(self.login_page,"Login")
