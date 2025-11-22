from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import os

from core.session_manager import Session
from core.session_task import Task_Session

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        Session.session_user_set.connect(self.reload_user)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

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
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            self.stats_layout.addWidget(label)
        layout.addLayout(self.stats_layout)

        # Task preview list
        self.recent_tasks_label = QLabel("<b>🧾 Recent Tasks:</b>")
        layout.addWidget(self.recent_tasks_label)
        self.task_list = QListWidget()
        self.task_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.task_list)
        self.card_widget = self.card("Some text")
        self.card_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(self.card_widget)

        layout.addStretch()
        self.apply_theme()
        self.reload_user()
    
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
        
        # Apply styles to stat labels
        if is_dark:
            stat_style = "background-color: #2d2d30; padding: 10px; border-radius: 10px; color: white;"
            list_style = """
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
            """
            card_style = """
                background-color: #2d2d30;
                padding: 15px;
                border-radius: 10px;
                color: white;
            """
        else:
            stat_style = "background-color: #f1f1f1; padding: 10px; border-radius: 10px; color: #1e1e1e;"
            list_style = """
                QListWidget {
                    background-color: #ffffff;
                    color: #1e1e1e;
                    border: 1px solid #ddd;
                    border-radius: 6px;
                }
                QListWidget::item {
                    padding: 8px;
                }
                QListWidget::item:selected {
                    background-color: #e6f0ff;
                }
            """
            card_style = """
                background-color: #f1f1f1;
                padding: 15px;
                border-radius: 10px;
                color: #1e1e1e;
            """
        
        for label in [self.label_total, self.label_completed, self.label_pending]:
            label.setStyleSheet(stat_style)
        
        self.task_list.setStyleSheet(list_style)
        if hasattr(self, "card_widget"):
            self.card_widget.setStyleSheet(card_style)

    def card(self, text):
        label = QLabel(text)
        label.setWordWrap(True)
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
