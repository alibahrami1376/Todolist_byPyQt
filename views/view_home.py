from PyQt6.QtWidgets import (
    QMainWindow,QWidget, QVBoxLayout, QPushButton, QListWidget,
    QMessageBox, QListWidgetItem, QHBoxLayout, QCheckBox,QLineEdit,QMenu
)
from PyQt6.QtCore import Qt,QSize,QDate
from PyQt6.QtGui import QIcon,QFont


from views.view_addtask import AddTaskWindow
from views.view_pagemanager import PageManagerWindow
from models.task_models import TaskModel
from viewmodels.task_view_models import TaskViewModel
from utils.stylesheet_loader import load_stylesheet


class TaskManagerWindow(QMainWindow):
    def __init__(self,manager : PageManagerWindow):
        """ Initialize the home-task manager window """
        super().__init__()
        self.viewmodel :TaskViewModel
        self.manager = manager

        self.init_ui()

        
    def set_user(self, user_id: str):
        self.viewmodel = TaskViewModel(user_id)
        self.load_tasks()

    def load_tasks(self):
        self.task_list.clear()
        tasks = self.viewmodel.get_all_tasks()
        if tasks:
            for task in tasks:
                self.create_task_item_widget(task)


    def init_ui(self):
        """ Initialize the page components """  
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.create_inputlayout()
        layout.addLayout(self.input_layout)

        self.create_task_list()
        layout.addWidget(self.task_list)

        self.create_btn_control()
        self.create_menu_right_click()

        layout.addLayout(self.btn_layout)
        
        self.setCentralWidget(central_widget)


    def create_inputlayout(self):
        
        self.input_layout   = QHBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter the new task...")

        self.task_input.returnPressed.connect(self.add_task_to_list)
        self.input_layout.addWidget(self.task_input)

        add_task_btn = QPushButton()
        add_task_btn.setIcon(QIcon('images/add.png'))
        add_task_btn.clicked.connect(self.add_task_to_list)
        add_task_btn.setFixedWidth(70)
        add_task_btn.setStyleSheet(load_stylesheet("styles/home/button_add.qss"))
        self.input_layout.addWidget(add_task_btn)

        more_task_btn = QPushButton()
        more_task_btn.setIcon(QIcon('images/more.png'))
        more_task_btn.clicked.connect(self.open_add_task_window)
        more_task_btn.setFixedWidth(30)
        more_task_btn.setStyleSheet(load_stylesheet("styles/home/button_more.qss"))
        self.input_layout.addWidget(more_task_btn)


    def create_task_list(self):
       
        self.task_list = QListWidget()
        self.task_list.setStyleSheet(load_stylesheet("styles/home/list.qss"))
        self.task_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self.right_click_menu)


    def create_btn_control(self): 

        self.btn_layout = QHBoxLayout()
        
        remove_selected_btn = QPushButton("❌Delete selected task" )
        remove_selected_btn.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))  
        remove_selected_btn.clicked.connect(self.remove_selected_task)
        remove_selected_btn.setStyleSheet(load_stylesheet("styles/home/button_re_sel.qss"))
        self.btn_layout.addWidget(remove_selected_btn)

        clear_btn = QPushButton("🗑️Clear All")
        clear_btn.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
        clear_btn.clicked.connect(self.clear_all_tasks)
        clear_btn.setStyleSheet(load_stylesheet("styles/home/button_dell_all.qss"))
        self.btn_layout.addWidget(clear_btn)


    def open_add_task_window(self):
        #self.new_task = TaskModel() 
        self.add_task_window = AddTaskWindow()
        self.add_task_window.signal_saved.connect(self.handle_new_task)
        self.add_task_window.exec()


    def handle_new_task(self, task: TaskModel):
        self.viewmodel.add_task(task)
        self.create_task_item_widget(task)
     

    def add_task_to_list(self):

        title = self.task_input.text().strip()

        if not title:
            self.show_warning( "The task title cannot be empty.")
            return
        
        task_new = self.create_task_just_titel(title)
        self.viewmodel.add_task(task_new)
        self.create_task_item_widget(task_new)
        self.task_input.clear()


    def create_task_just_titel(self,title:str) -> TaskModel:
        """ Create a task with just the title """
        task = TaskModel(
            title=title,
            description="",
            priority = "middle",
            due_date=QDate().currentDate().toPyDate(),
            completed=False)
        return task
    

    def create_task_item_widget(self, task: TaskModel) -> None:
        """ Create a task item widget with checkbox """
    
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, task)
        checkbox = self.build_checkbox_for_task(task, item)
        self.task_list.addItem(item)
        item.setSizeHint(checkbox.sizeHint()+ QSize(10, 10)) 
        self.task_list.setItemWidget(item, checkbox)
        

    def format_task_text(self, task:TaskModel):
        """ Format the task text for display """
        return f"{task.title} | priority: {task.priority} | date: {task.due_date}\n{task.description}"


    def check_task_checkbox_strikeout(self,checkbox: QCheckBox)->QCheckBox:
        is_checked = checkbox.isChecked()
        font = checkbox.font()
        font.setStrikeOut(is_checked)
        checkbox.setFont(font)
        return checkbox


    def task_toggle_checkbox(self, checkbox : QCheckBox,item :QListWidgetItem):
        """ Toggle the task completion status and strikeout the text """

        checkbox = self.check_task_checkbox_strikeout(checkbox)
        task: TaskModel = item.data(Qt.ItemDataRole.UserRole)
        task.completed = checkbox.isChecked()
        self.viewmodel.mark_toggel(task, task.completed)

    
    def edit_selected_task(self):
        """ Edit the selected task """
        selected = self.task_list.currentItem()
        task : TaskModel = selected.data(Qt.ItemDataRole.UserRole)
        task = self.viewmodel.find_by_id(task.id)
        if selected:
            self.edit_window = AddTaskWindow(task, edit_mode=True)
            self.edit_window.signal_saved.connect(lambda updated_task: self.handle_save_task(updated_task, selected))
            self.edit_window.exec()

        else:
            self.show_warning("Please select a task to edit.")


    def handle_save_task(self, task: TaskModel,item: QListWidgetItem):
        """ Handle the save task signal from the edit window """
        if task:
            self.viewmodel.update_task(task)
            self.update_task_in_list(task,item)
        else:
            self.show_warning("Please select a task to edit.")


    def update_task_in_list(self, updated_task: TaskModel, item: QListWidgetItem):
        
        item.setData(Qt.ItemDataRole.UserRole, updated_task)
        checkbox = self.build_checkbox_for_task(updated_task, item)
        item.setSizeHint(checkbox.sizeHint()+ QSize(10, 10))
        self.task_list.setItemWidget(item, checkbox)


    def remove_selected_task(self):
        """ Remove the selected task from the list """
        selected = self.task_list.currentItem()
       
        
        if selected:
            if self.show_question("Confirmation", f"Are you sure you want to delete task?"):
                row  = self.task_list.row(selected)  
                item = self.task_list.takeItem(row)
                task : TaskModel = item.data(Qt.ItemDataRole.UserRole)
                self.viewmodel.delete_task(task.id)
        else :
            self.show_warning("Please select a task to delete.")
            return
            
        
    def show_warning(self, message: str):
        """ Show a warning message """
        QMessageBox.warning(self, "Warning", message, QMessageBox.StandardButton.Ok)


    def show_question(self, title: str , message: str)-> bool:
    
        """ Show a question message """
        reply = QMessageBox.question(self,
                            title,
                            message,
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                            )
        if reply == QMessageBox.StandardButton.Yes:
            return True
        else:
            return False    


    def create_menu_right_click(self):
        """ Create a right-click menu for the task list """
        self.menu_right_click = QMenu()
        self.delete_action = self.menu_right_click.addAction("Delete task")
        self.edite_action = self.menu_right_click.addAction("Edit task")


    def right_click_menu(self, position):

        action =self.menu_right_click.exec(self.task_list.viewport().mapToGlobal(position))

        if action == self.delete_action:
            self.remove_selected_task()
        elif action == self.edite_action:
                self.edit_selected_task()


    def clear_all_tasks(self):
        """ Clear all tasks from the list """
        if self.show_question("Confirmation", "Are you sure you want to delete all tasks?"):
            self.viewmodel.clear_all()
            self.task_list.clear()
        return
        
    def build_checkbox_for_task(self, task: TaskModel, item: QListWidgetItem) -> QCheckBox:
        checkbox = QCheckBox(self.format_task_text(task))
        checkbox.setChecked(task.completed)
        checkbox.setStyleSheet("padding: 5px;")
        
        checkbox.stateChanged.connect(lambda state, cb=checkbox, it=item: self.task_toggle_checkbox(cb, it))
        return self.check_task_checkbox_strikeout(checkbox)