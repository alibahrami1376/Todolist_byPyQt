from typing import Optional

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox,
    QTextEdit, QPushButton, QDateEdit, QMessageBox, QCheckBox
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QPalette, QColor,QFont
from PyQt6.QtCore import pyqtSignal


from models.task_models import TaskModel
from utils.stylesheet_loader import load_stylesheet

class AddTaskWindow(QDialog):
    signal_saved = pyqtSignal(TaskModel)
    
    def __init__(self, task : Optional[TaskModel]=None,parent = None ,edit_mode = False):
        super().__init__(parent)

        self.setWindowTitle("Add new task" if not edit_mode else "Edit Task")
        self.setFixedSize(420, 440)
    
        self.task_data = task
        self.edit_mode = edit_mode

        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()

        self.create_title_input(layout)
        self.create_description_input(layout)
        self.create_priority_input(layout)
        self.create_due_data_input(layout)
        self.create_checkbox(layout,"The subset is a task.")
        self.create_save_button("save",layout)

        self.setLayout(layout)

        if self.edit_mode and self.task_data:
            self.load_data()


    def create_title_input(self,layout:QVBoxLayout):

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Task title")
        self.title_input.setStyleSheet(load_stylesheet("styles/addtask/title_input.qss"))
        layout.addWidget(QLabel("Task title:"))
        layout.addWidget(self.title_input)
        

    def create_save_button(self,label : str,layout : QVBoxLayout):
        self.save_button = QPushButton(label)
        self.save_button.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold)) 
        self.save_button.setStyleSheet(load_stylesheet("styles/addtask/button_save.qss"))
        self.save_button.clicked.connect(self.save_task)
        layout.addWidget(self.save_button)


    def create_description_input(self,layout: QVBoxLayout):
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description")
        self.description_input.setStyleSheet(load_stylesheet("styles/addtask/description.qss"))
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)


    def create_priority_input(self,layout:QVBoxLayout):
        self.priority_input = QComboBox()
        self.priority_input.setStyleSheet(load_stylesheet("styles/addtask/priority.qss"))
        self.priority_input.addItems(["Low", "Middle", "Top"])
        layout.addWidget(QLabel("priority"))
        layout.addWidget(self.priority_input)


    def create_due_data_input(self,layout:QVBoxLayout):
        self.due_date_input = QDateEdit()
        self.due_date_input.setStyleSheet(load_stylesheet("styles/addtask/due_date.qss"))
        self.due_date_input.setDate(QDate.currentDate())
        self.due_date_input.setCalendarPopup(True)
        layout.addWidget(QLabel("due date"))
        layout.addWidget(self.due_date_input)


    def create_checkbox(self,layout:QVBoxLayout,text : str):
        self.is_subtask_checkbox = QCheckBox(text)
        layout.addWidget(self.is_subtask_checkbox)


    def load_data(self):
        self.title_input.setText(self.task_data.title)
        self.description_input.setText(self.task_data.description)
        self.priority_input.setCurrentText(self.task_data.priority)
        date = QDate.fromString(self.task_data.due_date, "yyyy-MM-dd")
        if date.isValid():
            self.due_date_input.setDate(date)
        self.is_subtask_checkbox.setChecked(self.task_data.is_subtask)


    def show_warning(self, message: str):
        QMessageBox.warning(self, "Warning", message, QMessageBox.StandardButton.Ok)


    def save_task(self):
        """ Handle saving task based on mode """
        title = self.title_input.text().strip()
        if not title:
            self.show_warning("Please enter a title for the task.")
            return

        if not self.edit_mode:
            self.save_new_task(title)
        else:
            self.update_existing_task(title)

        self.accept()


    def save_new_task(self, title: str):
        task = TaskModel(
            title=title,
            description=self.description_input.toPlainText(),
            priority=self.priority_input.currentText(),
            due_date=self.due_date_input.date().toString("yyyy-MM-dd"),
            is_subtask=self.is_subtask_checkbox.isChecked(),
            completed=False
        )
        self.signal_saved.emit(task)


    def update_existing_task(self, title: str):
        assert self.task_data is not None
        self.task_data.title = title
        self.task_data.description = self.description_input.toPlainText()
        self.task_data.priority = self.priority_input.currentText()
        self.task_data.due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        self.task_data.is_subtask = self.is_subtask_checkbox.isChecked()
        self.signal_saved.emit(self.task_data)
    

