from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt
from models.task_models import TaskModel

class ShowTaskPage(QDialog):
    def __init__(self, task: TaskModel):
        super().__init__()

        self.task = task

        self.setWindowTitle("Task Details")
        self.setFixedSize(400, 400)
        self.setStyleSheet("""
            background-color: #1e1e1e;
            border-radius: 16px;
            color: white;
            font-family: Segoe UI;
            font-size: 14px;
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # عنوان تسک
        title_label = QLabel(f"<b>Title:</b> {self.task.title}")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # توضیحات
        description_label = QLabel(f"<b>Description:</b><br>{self.task.description}")
        description_label.setWordWrap(True)
        layout.addWidget(description_label)

        # اولویت
        priority_label = QLabel(f"<b>Priority:</b> {self.task.priority}")
        layout.addWidget(priority_label)

        # تاریخ سررسید
        due_date_label = QLabel(f"<b>Due Date:</b> {self.task.due_date}")
        layout.addWidget(due_date_label)

        # وضعیت انجام شده
        completed_label = QLabel(f"<b>Completed:</b> {'✅ Done' if self.task.completed else '❌ Not Done'}")
        layout.addWidget(completed_label)

        layout.addStretch()

        # دکمه بستن
        btn_close = QPushButton("Close")
        btn_close.setFixedWidth(100)
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignCenter)
