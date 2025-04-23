from PyQt6.QtWidgets import QMessageBox, QWidget
from typing import Optional  
from PyQt6.QtWidgets import QMessageBox, QWidget

class AppNotifier:
    _instance = None

    def __new__(cls, parent: QWidget):
        if cls._instance is None:
            cls._instance = super(AppNotifier, cls).__new__(cls)
            cls._instance.parent = parent
        return cls._instance

    def set_parent(self, parent: QWidget):
        self.parent = parent

    def info(self, title: str, message: str):
        QMessageBox.information(self.parent, title, message, QMessageBox.StandardButton.Ok)

    def warning(self, title: str, message: str):
        QMessageBox.warning(self.parent, title, message, QMessageBox.StandardButton.Ok)

    def error(self, title: str, message: str):
        QMessageBox.critical(self.parent, title, message, QMessageBox.StandardButton.Ok)

    def confirm(self, title: str, message: str) -> bool:
        reply = QMessageBox.question(
            self.parent,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
