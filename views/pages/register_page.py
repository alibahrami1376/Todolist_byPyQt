from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFormLayout, QMessageBox, QHBoxLayout, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import pyqtSignal, Qt, QPoint
from PyQt6.QtGui import QMouseEvent, QColor, QFont
import os

from utils.app_notifier import AppNotifier


class RegisterPage(QDialog):
    register_submitted = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 500)
        self.resize(450, 550)  # Set initial size but allow resize
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.old_pos = None
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
        self.setStyleSheet(self.load_styles(is_dark))
        if hasattr(self, "container_frame"):
            if is_dark:
                self.container_frame.setStyleSheet("background-color: #1e1e1e; border-radius: 16px;")
                if hasattr(self, "title_label"):
                    self.title_label.setStyleSheet("color: #BB86FC;")
                if hasattr(self, "close_btn"):
                    self.close_btn.setStyleSheet("background-color: transparent; color: white; border: none; font-size: 16px;")
            else:
                self.container_frame.setStyleSheet("background-color: #ffffff; border-radius: 16px; border: 1px solid #ddd;")
                if hasattr(self, "title_label"):
                    self.title_label.setStyleSheet("color: #2b59c3;")
                if hasattr(self, "close_btn"):
                    self.close_btn.setStyleSheet("background-color: transparent; color: #1e1e1e; border: none; font-size: 16px;")
        
        

    def init_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        self.container_frame = QFrame()
        container_layout = QVBoxLayout(self.container_frame)
        container_layout.setContentsMargins(40, 30, 40, 20)
        container_layout.setSpacing(20)

        # Title Bar
        title_bar = QHBoxLayout()
        self.title_label = QLabel("Create Account")
        self.title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self.close)
        title_bar.addWidget(self.title_label)
        title_bar.addStretch()
        title_bar.addWidget(self.close_btn)
        container_layout.addLayout(title_bar)

        # Form Fields
        form_layout = QFormLayout()
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout.setSpacing(16)

        self.username_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.password_input = QLineEdit()

        fields = [
            ("Username", self.username_input),
            ("Email", self.email_input),
            ("Phone", self.phone_input),
            ("Password", self.password_input),
        ]

        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        for label, widget in fields:
            widget.setPlaceholderText(label)
            widget.returnPressed.connect(self.handle_submit)
            widget.setFixedHeight(48)
            widget.setFont(QFont("Segoe UI", 10))
            add_shadow(widget)
            form_layout.addRow(widget)

        container_layout.addLayout(form_layout)

        # Submit Button
        submit_btn = QPushButton("Register")
        submit_btn.setObjectName("register_btn")
        submit_btn.setFixedHeight(48)
        add_shadow(submit_btn)
        submit_btn.clicked.connect(self.handle_submit)
        container_layout.addWidget(submit_btn)

        container_layout.addStretch()
        outer_layout.addWidget(self.container_frame)

    def handle_submit(self):
        data = {
            "username": self.username_input.text().strip(),
            "email": self.email_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "password": self.password_input.text().strip(),
        }

        if not all(data.values()):
            AppNotifier(self).warning("Missing Fields", "Please fill in all fields.")
            return

        self.register_submitted.emit(data)
        AppNotifier(self).info(title="Success", message="Account created successfully.")
        self.accept()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def load_styles(self, is_dark=True):
        if is_dark:
            return """
            QLineEdit {
                background-color: #2C2C2C;
                border: 2px solid #3E3E3E;
                border-radius: 20px;
                padding: 12px;
                color: #FFFFFF;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #BB86FC;
                background-color: #1F1F1F;
            }
            QPushButton {
                background-color: #BB86FC;
                border-radius: 20px;
                color: white;
                font-size: 15px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #9B6DFF;
            }
            QPushButton:pressed {
                background-color: #7F39FB;
            }
            QLabel {
                color: #BB86FC;
            }
            """
        else:
            return """
            QLineEdit {
                background-color: #f6f6f6;
                border: 2px solid #cfcfcf;
                border-radius: 20px;
                padding: 12px;
                color: #1e1e1e;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #2b59c3;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #2b59c3;
                border-radius: 20px;
                color: white;
                font-size: 15px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1e4a9e;
            }
            QPushButton:pressed {
                background-color: #153d7a;
            }
            QLabel {
                color: #2b59c3;
            }
            """



def add_shadow(widget):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(25)
    shadow.setOffset(0, 4)
    shadow.setColor(QColor(0, 0, 0, 130))
    widget.setGraphicsEffect(shadow)
