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
from views.pages.taskeditore_page import TaskEditorPage
from views.pages.showtask_pag import ShowTaskPage
from views.pages.fields_page import FieldsPage
from views.pages.field_one_page import FieldOnePage
from views.pages.field_two_page import FieldTwoPage
from views.pages.field_three_page import FieldThreePage
from views.pages.field_four_page import FieldFourPage
from views.pages.ideas_page import IdeasPage
from views.pages.projects_page import ProjectsPage
from views.pages.learning_paths_page import LearningPathsPage
from typing import Optional
from models.task_models import TaskModel

class PageRegistry:
    def __init__(self):
        self.dash= DashboardPage()
        self.calendar= CalendarPage()
        self.settings= SettingsPage()
        self.login= LoginPage()
        self.about= AboutPage()
        self.journal= JournalPage()
        self.timer= TimerPage()
        self.todo= TodoListPage()
        self.userdash= UserDashboardPage()
        self.register= RegisterPage()
        self.fields = FieldsPage(
            open_field_one=self.open_field_one,
            open_field_two=self.open_field_two,
            open_field_three=self.open_field_three,
            open_field_four=self.open_field_four,
        )
        self.ideas = IdeasPage()
        self.projects = ProjectsPage()
        self.learning_paths = LearningPathsPage()
        # self.editor= None

    # @property
    # def editor(self):
    #     if self.editor is None:
    #         self.editor = TaskEditorPage()
    #     return self.editor

    def edit_task(self,task:Optional[TaskModel]=None):
        return TaskEditorPage(task)
    def show_task(self,task:TaskModel):
        return ShowTaskPage(task)

    def open_field_one(self):
        dlg = FieldOnePage()
        dlg.exec()

    def open_field_two(self):
        dlg = FieldTwoPage()
        dlg.exec()

    def open_field_three(self):
        dlg = FieldThreePage()
        dlg.exec()

    def open_field_four(self):
        dlg = FieldFourPage()
        dlg.exec()
