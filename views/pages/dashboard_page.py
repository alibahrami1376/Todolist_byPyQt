from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from core.session_manager import Session
from core.session_task import Task_Session
from viewmodels.task_viewmodels import TaskViewModel

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        Session.session_user_set.connect(self.reload_user)
        # self.task_viewmodel = TaskViewModel()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.header_label = QLabel("<h2>📋 Dashboard</h2>")
        layout.addWidget(self.header_label)

        self.welcome_label = QLabel("<b>Welcome to your task dashboard!</b>")
        layout.addWidget(self.welcome_label)

        # Quick stats section
        self.stats_layout = QHBoxLayout()
        self.label_total = QLabel()
        self.label_completed = QLabel()
        self.label_pending = QLabel()
        for label in [self.label_total, self.label_completed, self.label_pending]:
            label.setStyleSheet("background-color: #2d2d30; padding: 10px; border-radius: 10px;")
            self.stats_layout.addWidget(label)
        layout.addLayout(self.stats_layout)

        # Task preview list
        layout.addWidget(QLabel("<b>🧾 Recent Tasks:</b>"))
        self.task_list = QListWidget()
        self.task_list.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #444;
                border-radius: 6px;
            }
            QListWidget::item {
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
            }
        """)
        layout.addWidget(self.task_list)
        layout.addWidget(self.card("Some text"))

        layout.addStretch()
        self.reload_user()

    def card(self, text):
        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet("""
            background-color: #2d2d30;
            padding: 15px;
            border-radius: 10px;
            color: white;
        """)
        return label

    def reload_user(self):
        user = Session.current_user()
        if user:
            self.welcome_label.setText(f"<b>Welcome back, {user.username}!</b>")
            tasks = Task_Session.get_all()
            self.task_list.clear()
            for task in tasks[:5]:
                self.task_list.addItem(QListWidgetItem(f"📌 {task.title}"))

            total = len(tasks)
            completed = len([t for t in tasks if t.completed])
            pending = total - completed

            self.label_total.setText(f"<b>📌 Total Tasks</b><br>{total}")
            self.label_completed.setText(f"<b>✅ Completed</b><br>{completed}")
            self.label_pending.setText(f"<b>⏳ Pending</b><br>{pending}")
        else:
            self.welcome_label.setText("<b>Welcome!</b>")
            self.task_list.clear()
            self.label_total.setText(f"<b>📌 Total Tasks</b><br>0")
            self.label_completed.setText(f"<b>✅ Completed</b><br>0")
            self.label_pending.setText(f"<b>⏳ Pending</b><br>0")
