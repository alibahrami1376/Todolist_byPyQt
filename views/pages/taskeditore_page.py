
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,QDialog,
    QComboBox, QDateEdit, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from models.task_models import TaskModel
from typing import Optional

from utils.stylesheet_loader import load_stylesheet
from utils.app_notifier import AppNotifier
from viewmodels.task_viewmodels import TaskViewModel

class TaskEditorPage(QDialog):
    task_saved = pyqtSignal(TaskModel)

    def __init__(self, task: Optional[TaskModel] = None):
        super().__init__()

        self.setWindowTitle("Task Editor")
        self.TaskViewmodel= TaskViewModel()
        self.task= task
        self.flag_edit= False if self.task is None else True
        self.init_ui()
        self.load_task()
        self.setStyleSheet("""
        background-color: #1e1e1e;
        border-radius: 16px;
        """)

    def init_ui(self):
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        
        # عنوان
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Task Title")
        self.title_input.setStyleSheet(load_stylesheet("styles/addtask/title_input.qss"))
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_input)

        # توضیحات
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description...")
        self.description_input.setStyleSheet(load_stylesheet("styles/addtask/description.qss"))
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)

        # اولویت
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Middle", "High"])
        self.priority_input.setStyleSheet(load_stylesheet("styles/addtask/priority.qss"))
        layout.addWidget(QLabel("Priority:"))
        layout.addWidget(self.priority_input)

        # تاریخ سررسید
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDate(QDate.currentDate())
        self.due_date_input.setStyleSheet(load_stylesheet("styles/addtask/due_date.qss"))
        layout.addWidget(QLabel("Due Date:"))
        layout.addWidget(self.due_date_input)

        # دکمه ذخیره
        save_button = QPushButton("Save Task")
        save_button.clicked.connect(self.handle_save)
        save_button.setStyleSheet(load_stylesheet("styles/addtask/button_save.qss"))
        layout.addWidget(save_button)
        layout.addStretch()

    def load_task(self):
        """
        اگر تسکی پاس داده شده، فیلدها رو پر کن
        """
        if not self.task:
            return
        
        self.title_input.setText(self.task.title)
        self.description_input.setText(self.task.description)
        self.priority_input.setCurrentText(self.task.priority)
        self.due_date_input.setDate(self.task.due_date)

    def handle_save(self):
        """
        ذخیره اطلاعات و ارسال سیگنال
        """
        _titel = self.title_input.text().strip()
        if not _titel :
            AppNotifier(QWidget).warning("warning","Title is required!")
            return

        task = self.task or TaskModel(_titel) # اگر قبلاً تسک وجود نداشت، جدید بساز
        task.title = self.title_input.text().strip()
        task.description = self.description_input.toPlainText().strip()
        task.priority = self.priority_input.currentText()
        task.due_date = self.due_date_input.date().toPyDate()

        self.task_saved.emit(task)  # ارسال به کنترلر یا ویومدل
        self.accept()
