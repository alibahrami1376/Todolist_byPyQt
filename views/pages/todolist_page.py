from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QListWidgetItem, QCheckBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

class TodoListPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel("📝 Todo List")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        self.input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        self.task_input.setFixedHeight(35)
        self.task_input.returnPressed.connect(self.add_task)
        self.input_layout.addWidget(self.task_input)

        self.add_button = QPushButton("Add")
        self.add_button.setFixedHeight(35)
        self.add_button.clicked.connect(self.add_task)
        self.input_layout.addWidget(self.add_button)

        layout.addLayout(self.input_layout)

        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

    def add_task(self):
        text = self.task_input.text().strip()
        if text:
            item = QListWidgetItem()
            checkbox = QCheckBox(text)
            checkbox.stateChanged.connect(lambda: self.toggle_strike(checkbox))
            checkbox.setStyleSheet("padding: 5px;")
            item.setSizeHint(QSize(0, 30))
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, checkbox)
            self.task_input.clear()

    def toggle_strike(self, checkbox):
        font = checkbox.font()
        font.setStrikeOut(checkbox.isChecked())
        checkbox.setFont(font)
