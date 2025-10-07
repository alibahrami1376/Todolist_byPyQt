
from PyQt6.QtCore import QObject
from views.pages.todolist_page import TodoListPage
from views.main_frameless_window import MainFramelessWindow
from core.session_manager import Session
from core.session_task import Task_Session
from views.pages.taskeditore_page import TaskEditorPage
from models.task_models import TaskModel
from views.pages.showtask_pag import ShowTaskPage
from services.task_service import TaskService
from mapper.task_mapper import map_model_to_entity_by_userid, map_entity_to_model, map_model_to_entity


class TaskController(QObject):
    def __init__(self,
                 page_todolist: TodoListPage,
                 page_editore,
                 page_manager: MainFramelessWindow,
                 page_showtask):
        super().__init__()
        self.page_todolist = page_todolist
        self.page_editore = page_editore
        self.page_manager = page_manager
        self.page_showtask = page_showtask
        self.task_service = TaskService()
        self._connect_signals()

    def _connect_signals(self):
        pt = self.page_todolist
        pt.handle_quick_add.connect(self.handel_quick_tasknew)
        pt.handle_load_user_task.connect(self.handle_loding_tasks)
        pt.handle_edite_window.connect(self.handle_edite_window)
        pt.handle_tasknew_window.connect(self.handle_tasknew_window)
        pt.handle_toggle_checkbox.connect(self.handle_toggle_checkbox)
        pt.handle_delet_task.connect(self.handle_delete_task)
        pt.handle_show_task.connect(self.handle_show_task)
        self.page_manager.handle_exit.connect(self.handle_exit)

    def _add_task_to_db(self, task: TaskModel):
        if not Session.is_guest():
            self.task_service.add(map_model_to_entity_by_userid(task, Session.get_id_user()))

    def handel_quick_tasknew(self, titel: str):
        task = TaskModel(titel)
        self._add_task_to_db(task)
        Task_Session.add_task(task)

    def handle_loding_tasks(self):
        if Session.is_guest():
            from services.task_js_storage import TaskJsonStorage
            tasks = TaskJsonStorage().load_all()
            Task_Session.load_tasks(tasks)
        else:
            entities = self.task_service.get_tasks_by_user(Session.get_id_user())
            Task_Session.load_tasks([map_entity_to_model(e) for e in entities])

    def handle_edite_window(self, task: TaskModel):
        editor_dialog: TaskEditorPage = self.page_editore(task)
        editor_dialog.task_saved.connect(self.event_editetask)
        editor_dialog.exec()

    def event_editetask(self, task: TaskModel):
        Task_Session.update_task(task)
        if not Session.is_guest():
            self.task_service.update(map_model_to_entity(task))

    def handle_tasknew_window(self):
        editor_dialog: TaskEditorPage = self.page_editore()
        editor_dialog.task_saved.connect(self.event_newtask)
        editor_dialog.exec()

    def event_newtask(self, task: TaskModel, flag: bool):
        self._add_task_to_db(task)
        Task_Session.add_task(task)

    def handle_toggle_checkbox(self, task: TaskModel, toggel_box: bool):
        task.completed = toggel_box
        Task_Session.update_task(task)
        if not Session.is_guest():
            self.task_service.update(map_model_to_entity(task))

    def handle_delete_task(self, task: TaskModel):
        task_id = task.id
        if not Session.is_guest():
            self.task_service.delete(task_id)
        Task_Session.remove_task(task_id)

    def handle_show_task(self, task: TaskModel):
        page_show: ShowTaskPage = self.page_showtask(task)
        page_show.exec()

    def handle_exit(self):
        if Session.is_guest():
            from services.task_js_storage import TaskJsonStorage
            TaskJsonStorage().save_all(Task_Session.get_all())

