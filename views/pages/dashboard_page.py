from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        layout.addWidget(QLabel("<h2>📋 Dashboard</h2>"))
        layout.addWidget(QLabel("<b>Welcome to your task dashboard!</b>"))

        # Quick stats section
        stats_layout = QHBoxLayout()
        for label, icon in [("Total Tasks", "📌"), ("Completed", "✅"), ("Pending", "⏳")]:
            stat = QLabel(f"<b>{icon} {label}</b><br>0")
            stat.setStyleSheet("background-color: #2d2d30; padding: 10px; border-radius: 10px;")
            stats_layout.addWidget(stat)
        layout.addLayout(stats_layout)

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

        # Load some placeholder tasks
        self.load_demo_tasks()
        layout.addStretch()

    def load_demo_tasks(self):
        tasks = ["Finish UI layout", "Connect database", "Test login flow", "Review project plan"]
        for task in tasks:
            item = QListWidgetItem(f"📌 {task}")
            self.task_list.addItem(item)
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
