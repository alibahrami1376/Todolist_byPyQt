from PyQt6.QtWidgets import (
    QMainWindow,QWidget, QVBoxLayout, QPushButton, QListWidget,
    QMessageBox, QListWidgetItem, QHBoxLayout, QCheckBox,QLineEdit,QMenu
)
from PyQt6.QtCore import Qt,QSize,QDate
from PyQt6.QtGui import QIcon, QPalette, QColor,QFont


from views.view_addtask import AddTaskWindow
from views.view_pagemanager import PageManagerWindow
from models.task_models import TaskModel


class TaskManagerWindow(QMainWindow):
    def __init__(self,manager : PageManagerWindow):
        super().__init__()
        self.manager = manager
        self.setWindowTitle("Task Manager-Todo List")
        self.setFixedSize(450, 600)
        self.setWindowIcon(QIcon('images/checklist.png')) 
        self.setDarkTheme()
        self.init_ui()
        self.create_menu_right_click()
        

    def init_ui(self):
        """ Initialize the page components """  
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.create_inputlayout()
        layout.addLayout(self.input_layout)

        self.create_task_list()
        layout.addWidget(self.task_list)

        self.create_btn_control()
        layout.addLayout(self.btn_layout)
        # ایجاد منوی بالا
        
        self.setCentralWidget(central_widget)


    def create_inputlayout(self):
        
        self.input_layout   = QHBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter the new task...")
        self.task_input.setStyleSheet("""
            background-color: #FFFFFF; 
            color: #000000; 
            padding: 8px; 
            border-radius: 5px;
        """)
        self.task_input.returnPressed.connect(self.add_task_to_list)
        self.input_layout.addWidget(self.task_input)

        add_task_btn = QPushButton()
        add_task_btn.setIcon(QIcon('images/add.png'))
        add_task_btn.clicked.connect(self.add_task_to_list)
        add_task_btn.setFixedWidth(70)
        add_task_btn.setStyleSheet("""
            QPushButton {
                background-color: #21A179;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #1B8060;
            }
        """)
        self.input_layout.addWidget(add_task_btn)

        more_task_btn = QPushButton()
        more_task_btn.setIcon(QIcon('images/more.png'))
        more_task_btn.clicked.connect(self.open_add_task_window)
        more_task_btn.setFixedWidth(30)
        more_task_btn.setStyleSheet("""
            QPushButton {
                background-color: #21A179;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #1B8060;
            }
        """)
        self.input_layout.addWidget(more_task_btn)


    def create_task_list(self):
        # لیست تسک‌ها
        self.task_list = QListWidget()
        self.task_list.setStyleSheet("""
            QListWidget {
                background-color: #3A3F4B;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
            }
            QListWidget::item {
                padding: 8px;
                margin: 3px;
                border-radius: 5px;
            }
            QListWidget::item:selected {
                background-color: #525966;
            }
        """)
        self.task_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self.right_click_menu)


    def create_btn_control(self): 
        # دکمه‌های کنترلی
        self.btn_layout = QHBoxLayout()
        
        remove_selected_btn = QPushButton("❌Delete selected task" )
        remove_selected_btn.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))  
        remove_selected_btn.clicked.connect(self.remove_selected_task)
        remove_selected_btn.setStyleSheet("""
            QPushButton {
                background-color: #D9534F;
                color: black;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #C9302C;
            }
        """)
        self.btn_layout.addWidget(remove_selected_btn)

        clear_btn = QPushButton("🗑️Clear All")
        clear_btn.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
        clear_btn.clicked.connect(self.clear_all_tasks)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #F0AD4E;
                color: black;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #EC971F;
            }
        """)
        self.btn_layout.addWidget(clear_btn)


    def setDarkTheme(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setPalette(palette)


    def open_add_task_window(self):
        self.add_task_window = AddTaskWindow(self)
        self.add_task_window.exec()

    
    def add_task_to_list(self):

        title = self.task_input.text().strip()

        if not title:
            self.show_warning( "The task title cannot be empty.")
            return
        
        date = QDate().currentDate().toString("yyyy-MM-dd")
        task = TaskModel(
            title=title,
            description="",
            priority = "middle",
            due_date=date,
            completed=False)
        
        self.create_task_item_widget(task)
        

    def more_add_task_to_list(self, task_details:TaskModel) -> None:
        """ Add a task to the list with more details """
        self.create_task_item_widget(task_details)
    

    def create_task_item_widget(self, task: TaskModel) -> None:
        """ Create a task item widget with checkbox """
        item = QListWidgetItem()
        checkbox = QCheckBox(self.format_task_text(task))
        checkbox.setStyleSheet("padding:5px;")
        checkbox.setChecked(task.completed)
        checkbox.stateChanged.connect(lambda: self.toggle_task_complete(checkbox))
        item.setSizeHint(checkbox.sizeHint() + QSize(10, 20))
        self.task_list.addItem(item)
        self.task_list.setItemWidget(item, checkbox)
        

    def format_task_text(self, task:TaskModel):
        """ Format the task text for display """
        return f"{task.title} | priority: {task.priority} | date: {task.due_date}\n{task.description}"


    def toggle_task_complete(self, checkbox):
        """ Toggle the task completion status and strikeout the text """
        font = checkbox.font()
        font.setStrikeOut(checkbox.isChecked())
        checkbox.setFont(font)


    def edit_selected_task(self):
        """ Edit the selected task """
        selected_item = self.task_list.currentItem()
        if selected_item:
            task_data = selected_item.text()
            self.edit_window = AddTaskWindow(self, task_data, edit_mode=True)
            self.edit_window.show()
        else:
            self.show_warning("Please select a task to edit.")


    def update_task_in_list(self, new_task_data):
        """ Update the task in the list with the new data """
        selected_item = self.task_list.currentItem()
        if selected_item:
            selected_item.task_data = new_task_data
            checkbox = QCheckBox(self.format_task_text(new_task_data))
            checkbox.stateChanged.connect(lambda: self.toggle_task_complete(checkbox))
            selected_item.setSizeHint(checkbox.sizeHint())
            self.task_list.setItemWidget(selected_item, checkbox)


    def remove_selected_task(self):
        """ Remove the selected task from the list """
        selected = self.task_list.currentRow()
        if selected >= 0:
            self.task_list.takeItem(selected)
        else:
            self.show_warning("Please select a task to delete.")


    def show_warning(self, message: str):
        """ Show a warning message """
        QMessageBox.warning(self, "Warning", message, QMessageBox.StandardButton.Ok)

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
        self.task_list.clear()
