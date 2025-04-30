from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QMenu,
    QLineEdit, QListWidget, QListWidgetItem, QCheckBox
)
from PyQt6.QtCore import Qt, QSize,QDate,pyqtSignal
from PyQt6.QtGui import QFont,QIcon
from models.task_models import TaskModel
from utils.app_notifier import AppNotifier
from utils.stylesheet_loader import load_stylesheet

from core.session_manager import Session
from core.session_task import Task_Session

class TodoListPage(QWidget):
    handle_quick_add= pyqtSignal(str)
    handle_edite_window= pyqtSignal(TaskModel)
    handle_load_user_task= pyqtSignal()
    handle_tasknew_window= pyqtSignal()
    handle_toggle_checkbox= pyqtSignal(TaskModel,bool)
    handle_delet_task= pyqtSignal(TaskModel)
    handle_show_task= pyqtSignal(TaskModel) 
    def __init__(self):
        super().__init__()
        Session.session_user_set.connect(self.load_user_task)
        Session.session_user_logout.connect(self.clear_page)
        Task_Session.task_session_new.connect(self.create_task_item_widget)
        Task_Session.task_session_edit.connect(self.update_task)
        Task_Session.task_session_remove.connect(self.refresh_page)
        self.init_ui()

    def init_ui(self):

        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("📝 Todo List")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        self.create_inputlayout()
        layout.addLayout(self.input_layout)

        self.create_task_list()
        self.create_menu_right_click()

        layout.addWidget(self.task_list)

        # self.create_btn_control()
        # self.create_menu_right_click()

        # layout.addLayout(self.btn_layout)
        
        # self.setCentralWidget(central_widget)
#-------------------------------------------------------
        # layout = QVBoxLayout(self)
        # layout.setContentsMargins(20, 20, 20, 20)
        # layout.setSpacing(10)

        # title = QLabel("📝 Todo List")
        # title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        # layout.addWidget(title)

        # self.input_layout = QHBoxLayout()
        # self.task_input = QLineEdit()
        # self.task_input.setPlaceholderText("Enter a new task...")
        # self.task_input.setFixedHeight(35)
        # self.task_input.returnPressed.connect(self.add_task)
        # self.input_layout.addWidget(self.task_input)

        # self.add_button = QPushButton("Add")
        # self.add_button.setFixedHeight(35)
        # self.add_button.clicked.connect(self.add_task)
        # self.input_layout.addWidget(self.add_button)

        # layout.addLayout(self.input_layout)

        # self.task_list = QListWidget()
        # layout.addWidget(self.task_list)


    def create_inputlayout(self):
        
        self.input_layout   = QHBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter the new task...")
        self.task_input.setFixedHeight(35)

        self.task_input.returnPressed.connect(self.quick_add)
        self.input_layout.addWidget(self.task_input)

        add_task_btn = QPushButton()
        add_task_btn.setIcon(QIcon('icons/add.png'))
        add_task_btn.clicked.connect(self.quick_add)
        add_task_btn.setFixedWidth(70)
        add_task_btn.setStyleSheet(load_stylesheet("styles/home/button_add.qss"))
        self.input_layout.addWidget(add_task_btn)

        more_task_btn = QPushButton()
        more_task_btn.setIcon(QIcon('icons/more.png'))
        more_task_btn.clicked.connect(self.tasknew_window)
        more_task_btn.setFixedWidth(30)
        more_task_btn.setStyleSheet(load_stylesheet("styles/home/button_more.qss"))
        self.input_layout.addWidget(more_task_btn)
 

    def create_task_list(self):
       
        self.task_list = QListWidget()
        self.task_list.setStyleSheet(load_stylesheet("styles/home/list.qss"))
        self.task_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self.right_click_menu)

    def create_menu_right_click(self):
        """ Create a right-click menu for the task list """
        dark_menu_style = """
                    QMenu {
                        background-color: #2d2d30;
                        color: white;
                        border: 1px solid #555;
                        padding: 5px;
                        border-radius: 10px;
                    }
                    QMenu::item {
                        background-color: transparent;
                        padding: 6px 24px;
                        border-radius: 6px;
                    }
                    QMenu::item:selected {
                        background-color: #0078d7;
                        color: white;
                    }
                    QMenu::separator {
                        height: 1px;
                        background: #555;
                        margin: 5px 10px;
                    }
                """
        self.menu_right_click = QMenu()
        self.menu_right_click.setStyleSheet(dark_menu_style)
        self.showtask_action = self.menu_right_click.addAction("Show Task")
        self.delete_action = self.menu_right_click.addAction("Delete Task")
        self.edite_action = self.menu_right_click.addAction("Edit Task")

    
    def right_click_menu(self, position):

        action =self.menu_right_click.exec(self.task_list.viewport().mapToGlobal(position))

        if action == self.delete_action:
            self.delete_task()
        elif action == self.edite_action:
            self.edite_window()
        elif action == self.showtask_action:
            self.show_task()
              

    def create_task_item_widget(self, task: TaskModel) -> None:
        """ Create a task item widget with checkbox """
    
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, task)
        checkbox = self.build_checkbox_for_task(task, item)
        self.task_list.addItem(item)
        item.setSizeHint(checkbox.sizeHint()+ QSize(30, 30)) 
        self.task_list.setItemWidget(item, checkbox)


    def quick_add(self):
        _titel = self.task_input.text().strip()
        if _titel:
            user =  Session.current_user()
            if user:
                self.handle_quick_add.emit(_titel)
                # self.create_task_item_widget(Task_Session.get_last_task())
                self.task_input.clear()
            else:
                AppNotifier(QWidget).warning("Log in","Please log in ")
        else:
            AppNotifier(QWidget).warning(title="warring",message="The task title cannot be empty.")

    def toggle_strike(self):
        selected = self.task_list.currentItem()
        checkbox: QCheckBox= self.task_list.itemWidget(selected)
        task: TaskModel = selected.data(Qt.ItemDataRole.UserRole)
        toggel_box = checkbox.isChecked()
        self.handle_toggle_checkbox.emit(task,toggel_box)


    def check_task_checkbox_strikeout(self,checkbox: QCheckBox)->QCheckBox:
        is_checked = checkbox.isChecked()
        font = checkbox.font()
        font.setStrikeOut(is_checked)
        checkbox.setFont(font)
        return checkbox

    def build_checkbox_for_task(self, task: TaskModel, item: QListWidgetItem) -> QCheckBox:
        checkbox = QCheckBox(self.format_task_text(task))
        checkbox.setChecked(task.completed)
        checkbox.setStyleSheet("padding: 5px;")
        checkbox.stateChanged.connect(self.toggle_strike)
        return self.check_task_checkbox_strikeout(checkbox)
    
  
    def format_task_text(self, task:TaskModel):
        """ Format the task text for display """
        return f"{task.title} | priority: {task.priority}"

    def load_user_task(self):
        self.handle_load_user_task.emit()
        self.refresh_page()
        
    def refresh_page(self):
        self.clear_page()
        tasks = Task_Session.get_all()
        if tasks:
            for task in tasks:
                self.create_task_item_widget(task)

    def clear_page(self):
        self.task_list.clear()
       
    def tasknew_window(self):
        user =  Session.current_user()
        if user:
            self.handle_tasknew_window.emit()       
        else:
            AppNotifier(QWidget).warning("Log in","Please log in ")

            
    def edite_window(self):
        user =  Session.current_user()
        if user:
            selected = self.task_list.currentItem()
            if selected:
                task : TaskModel = selected.data(Qt.ItemDataRole.UserRole)
                self.handle_edite_window.emit(task)
            else:
                AppNotifier(QWidget).warning("warning","Please select a task to edit.")
        else:
            AppNotifier(QWidget).warning("Log in","Please log in ")
                    
    def update_task(self,task):
        selected = self.task_list.currentItem()
        self.update_task_in_list(task,selected)

    
    def update_task_in_list(self, updated_task: TaskModel, item: QListWidgetItem):

        item.setData(Qt.ItemDataRole.UserRole, updated_task)
        checkbox = self.build_checkbox_for_task(updated_task, item)
        item.setSizeHint(checkbox.sizeHint()+ QSize(30, 30))
        self.task_list.setItemWidget(item, checkbox)
    
    def delete_task(self):

        selected = self.task_list.currentItem()
        if selected:
            task : TaskModel = selected.data(Qt.ItemDataRole.UserRole)
            confirm= AppNotifier(QWidget).confirm("Delete",f"Are you sure you want to permanently delet this {task.title}?")
            if confirm:
                self.handle_delet_task.emit(task)
        else:
            AppNotifier(QWidget).warning("warning","Please select a task to delete.")

    def show_task(self):
        selected = self.task_list.currentItem()
        if selected:
            task : TaskModel = selected.data(Qt.ItemDataRole.UserRole)
            self.handle_show_task.emit(task)  
        else:
            AppNotifier(QWidget).warning("warning","Please select a task to delete.") 
