from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox,
    QTextEdit, QPushButton, QDateEdit, QMessageBox, QCheckBox
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QPalette, QColor,QFont


from models.task_models import TaskModel

class AddTaskWindow(QDialog):
    def __init__(self, parent=None, task_data=None, edit_mode=False):
        super().__init__(parent)
        self.setWindowTitle("Add new task" if not edit_mode else "Edit Task")
        self.setFixedSize(420, 440)

        self.task_data = task_data
        self.edit_mode = edit_mode

        self.set_dark_theme()
        self.init_ui()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        self.setPalette(palette)

    def init_ui(self):

        layout = QVBoxLayout()

        self.create_title_ui(layout)
        self.create_description_input_ui(layout)
        self.create_priority_input_ui(layout)
        self.create_due_data_input_ui(layout)
        self.create_checkbox(layout,"The subset is a task.")
        self.create_pushbutton("save",layout)

        self.setLayout(layout)

        if self.edit_mode and self.task_data:
            self.load_data()

    def create_title_ui(self,layout:QVBoxLayout):

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Task title")
        self.title_input.setStyleSheet("""
            QLineEdit {
                background-color: #F2F2F2;
                color: black;
                border: 1px solid #E6E6E6;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(QLabel("Task title:"))
        layout.addWidget(self.title_input)
        

    def create_pushbutton(self,labale : str,layout : QVBoxLayout):

        self.save_button = QPushButton(labale)
        self.save_button.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold)) 
        self.save_button.setStyleSheet("""
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
        self.save_button.clicked.connect(self.save_task)
        layout.addWidget(self.save_button)

    def create_description_input_ui(self,layout: QVBoxLayout):

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description")
        self.description_input.setStyleSheet("""
            QTextEdit {
                background-color: #F2F2F2;
                color: black;
                border: 1px solid #E6E6E6;
            }                                 
        """)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)


    def create_priority_input_ui(self,layout:QVBoxLayout):
        self.priority_input = QComboBox()
        self.priority_input.setStyleSheet("""
            QComboBox {
                background-color: #F2F2F2;
                color: black;
                border: 1px solid #E6E6E6;
            }
        """)
        self.priority_input.addItems(["Low", "Middle", "Top"])
        layout.addWidget(QLabel("priority"))
        layout.addWidget(self.priority_input)


    def create_due_data_input_ui(self,layout:QVBoxLayout):
        self.due_date_input = QDateEdit()
        self.due_date_input.setStyleSheet("""
            QDateEdit {
                background-color: #F2F2F2;
                color: black;
                border: 1px solid #E6E6E6;
            }
        """)

        self.due_date_input.setDate(QDate.currentDate())
        self.due_date_input.setCalendarPopup(True)
        layout.addWidget(QLabel("due date"))
        layout.addWidget(self.due_date_input)

    def create_checkbox(self,layout:QVBoxLayout,text : str):
        self.is_subtask_checkbox = QCheckBox(text)
        layout.addWidget(self.is_subtask_checkbox)

    def load_data(self):
        self.title_input.setText(self.task_data.get('title', ''))
        self.description_input.setText(self.task_data.get('description', ''))
        self.priority_input.setCurrentText(self.task_data.get('priority', 'متوسط'))
        date_str = self.task_data.get('due_date', QDate.currentDate().toString("yyyy-MM-dd"))
        self.due_date_input.setDate(QDate.fromString(date_str, "yyyy-MM-dd"))
        self.is_subtask_checkbox.setChecked(self.task_data.get('is_subtask', False))

    def show_warning(self, message: str):
        """ Show a warning message """
        QMessageBox.warning(self, "Warning", message, QMessageBox.StandardButton.Ok)

    def save_task(self):
        title = self.title_input.text().strip()
        if not title:
            self.show_warning("Please enter a title for the task.")
            return
          
        task = TaskModel(
            title=title,
            description=self.description_input.toPlainText(),
            priority=self.priority_input.currentText(),
            due_date=self.due_date_input.date().toString("yyyy-MM-dd"),
            is_subtask=self.is_subtask_checkbox.isChecked(),
            completed=False
        )

        if hasattr(self.parent(), 'more_add_task_to_list'):
   
            self.parent().more_add_task_to_list(task)

        self.accept()
