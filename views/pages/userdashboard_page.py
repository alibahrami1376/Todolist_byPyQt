

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from core.session_manager import Session
from utils.app_notifier import AppNotifier

class UserDashboardPage(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        Session.session_user_set.connect(self.reload_user)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
                font-family: Segoe UI;
                font-size: 14px;
            }
            QFrame {
                background-color: #2d2d30;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #d9534f;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
        """)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)

        self.header = QLabel()
        self.header.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.layout.addWidget(self.header)

        self.profile_card = QFrame()
        self.profile_layout = QVBoxLayout(self.profile_card)
        self.label_username = QLabel()
        self.label_email = QLabel()
        self.label_phone = QLabel()

        self.profile_layout.addWidget(self.label_username)
        self.profile_layout.addWidget(self.label_email)
        self.profile_layout.addWidget(self.label_phone)
        self.layout.addWidget(self.profile_card)

        self.chart_section = QFrame()
        self.chart_layout = QVBoxLayout(self.chart_section)
        self.chart_layout.addWidget(QLabel("[Chart Placeholder: Task Completion, etc.]") )
        self.layout.addWidget(self.chart_section)

        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.handle_logout)
        self.layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignRight)
        self.layout.addStretch()

    def reload_user(self):
        user = Session.current_user()
        if user:
            self.header.setText(f"Welcome, {user.username}")
            self.label_username.setText(f"Username: {user.username}")
            self.label_email.setText(f"Email: {user.email_address}")
            self.label_phone.setText(f"Phone: {user.phone_number}")

    def handle_logout(self):
        if AppNotifier(QWidget).confirm("Logout",
            "Are you sure you want to log out of your account?"):
            self.logout_requested.emit()