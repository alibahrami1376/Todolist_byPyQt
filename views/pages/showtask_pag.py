from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt
from models.task_models import TaskModel
import os

class ShowTaskPage(QDialog):
    def __init__(self, task: TaskModel):
        super().__init__()

        self.task = task

        self.setWindowTitle("Task Details")
        self.setMinimumSize(400, 300)
        self.resize(450, 400)  # Set initial size but allow resize
        self.init_ui()
        self.apply_theme()
    
    def get_current_theme(self):
        """Get current theme from config"""
        config_path = "configg/theme_config.txt"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    theme = f.read().strip() or "روشن"
                    return theme == "دارک"
            except Exception:
                return True  # Default to dark
        return True  # Default to dark
    
    def apply_theme(self):
        """Apply theme based on current config"""
        is_dark = self.get_current_theme()
        if is_dark:
            self.setStyleSheet("""
                QDialog {
                    background-color: #1e1e1e;
                    border-radius: 16px;
                    color: white;
                    font-family: Segoe UI;
                    font-size: 14px;
                }
                QLabel {
                    color: white;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: #ffffff;
                    border-radius: 16px;
                    color: #1e1e1e;
                    font-family: Segoe UI;
                    font-size: 14px;
                }
                QLabel {
                    color: #1e1e1e;
                }
            """)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(18)
        layout.setContentsMargins(24, 24, 24, 24)

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
