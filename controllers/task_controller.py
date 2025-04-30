
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject,pyqtSignal



from views.pages.todolist_page import TodoListPage
from views.main_frameless_window import MainFramelessWindow

from core.session_manager import Session
from viewmodels.task_viewmodels import TaskViewModel
from utils.app_notifier import AppNotifier
from core.session_task import Task_Session
from views.pages.taskeditore_page import TaskEditorPage
from models.task_models import TaskModel
from views.pages.showtask_pag import ShowTaskPage

class TaskController(QObject):
    
    def __init__(
        self,
        page_todolist: TodoListPage,
        page_editore,
        page_manager: MainFramelessWindow,
        page_showtask
        ):
        super().__init__()
        self.page_todolist= page_todolist
        self.page_editore= page_editore
        self.page_manager = page_manager
        self.page_showtask = page_showtask
        self.task_viewmodel = TaskViewModel()
        self.connect_signals()

    def connect_signals(self):
        self.page_todolist.handle_quick_add.connect(self.handel_quick_tasknew)
        self.page_todolist.handle_load_user_task.connect(self.handle_loding_tasks)
        self.page_todolist.handle_edite_window.connect(self.handle_edite_window)
        self.page_todolist.handle_tasknew_window.connect(self.handle_tasknew_window)
        self.page_todolist.handle_toggle_checkbox.connect(self.handle_toggle_checkbox)
        self.page_todolist.handle_delet_task.connect(self.handle_delete_task)
        self.page_todolist.handle_show_task.connect(self.handle_show_task)
        self.page_manager.handle_exit.connect(self.handle_exit)


    def handel_quick_tasknew(self,titel:str):
            self.task_viewmodel.add_task_quick(titel)
       

    def handle_loding_tasks(self):
        if Session.is_guest():
           Task_Session.load_tasks(self.task_viewmodel.get_all_tasks_jason())     
        else:    
            Task_Session.load_tasks(self.task_viewmodel.get_all_tasks(Session.get_id_user())) 


    def handle_edite_window(self,task:TaskModel):
        editor_dialog : TaskEditorPage = self.page_editore(task)
        editor_dialog.task_saved.connect(self.event_editetask)
        editor_dialog.exec()
       
    def event_editetask(self,task):
        self.task_viewmodel.update_task(task)


    def handle_tasknew_window(self):
        editor_dialog : TaskEditorPage = self.page_editore()
        editor_dialog.task_saved.connect(self.event_newtask)
        editor_dialog.exec()
    

    def event_newtask(self,task: TaskModel,flag:bool):
        self.task_viewmodel.creat_task(task)
        

    def handle_toggle_checkbox(self,task: TaskModel,toggel_box: bool):
        task.completed = toggel_box 
        self.task_viewmodel.update_task(task)   


    def handle_delete_task(self,task:TaskModel):
        self.task_viewmodel.delete_task(task)


    def handle_show_task(self,task:TaskModel):
        page_show : ShowTaskPage = self.page_showtask(task)
        page_show.exec()
    

    def handle_exit(self):
        if Session.is_guest():
            self.task_viewmodel.save_tasks_jason()

