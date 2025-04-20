
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QDateTime

class JournalPage(QWidget):
    def __init__(self):
        super().__init__()

        self.entries = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        layout.addWidget(QLabel("<h2>📓 Journal</h2>"))

        # Entry list
        self.entry_list = QListWidget()
        self.entry_list.setStyleSheet("""
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
        layout.addWidget(self.entry_list, 1)

        # Editor area
        editor_frame = QFrame()
        editor_frame.setStyleSheet("background-color: #2d2d30; border-radius: 8px;")
        editor_layout = QVBoxLayout(editor_frame)

        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Write your thoughts here...")
        self.editor.setStyleSheet("padding: 10px; color: white;")
        editor_layout.addWidget(self.editor)

        # Save button
        save_btn = QPushButton("Save Entry")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005fa1;
            }
        """)
        save_btn.clicked.connect(self.save_entry)
        editor_layout.addWidget(save_btn)

        layout.addWidget(editor_frame, 2)

    def save_entry(self):
        content = self.editor.toPlainText().strip()
        if content:
            timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm")
            entry = f"[{timestamp}]\n{content}"
            self.entries.append(entry)
            item = QListWidgetItem(entry.split("\n")[0])
            self.entry_list.addItem(item)
            self.editor.clear()
