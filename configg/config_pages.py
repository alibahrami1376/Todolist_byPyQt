from configg.page_registery import PageRegistry
from controllers.auth_controller import AuthController
from views.main_frameless_window import MainFramelessWindow
from controllers.task_controller import TaskController
class ConfigPages:
    def __init__(self):
        self.pages = PageRegistry()
        self.window = MainFramelessWindow()
        self.add_page()
        self.auth = AuthController(
            login_page=self.pages.login,
            userdash_page=self.pages.userdash,
            register_page=self.pages.register,
            page_manager=self.window
        )
        self.task_controler = TaskController(
            page_todolist=self.pages.todo,
            page_showtask=self.pages.show_task,
            page_editore=self.pages.edit_task,
            page_manager=self.window
        ) 
    def add_page(self):             
        self.window.add_page(self.pages.dash,"Dashboard")
        self.window.add_page(self.pages.calendar,"Calendar")
        self.window.add_page(self.pages.settings, "Settings")
        self.window.add_page(self.pages.login, "Login")
        self.window.add_page(self.pages.about, "About")
        self.window.add_page(self.pages.journal, "Journal")
        self.window.add_page(self.pages.timer, "Timer")
        self.window.add_page(self.pages.todo, "TodoList")
        self.window.add_page(self.pages.userdash,"usdash")