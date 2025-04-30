from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGraphicsDropShadowEffect
)
from typing import Optional
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont

from utils.app_notifier import AppNotifier


class LoginPage(QWidget):
    TITLE_FONT = QFont("Segoe UI", 24, QFont.Weight.Bold)
    INPUT_HEIGHT = 48
    BUTTON_HEIGHT = 44
    login_requested = pyqtSignal(str, str)
    register_requested = pyqtSignal()
    guest_requested = pyqtSignal()

    def __init__(self,notifier: Optional[AppNotifier]= None) ->None:
        super().__init__()
        self.notifier = notifier or AppNotifier(self)
        self.setStyleSheet(self.load_styles())
        self.setAutoFillBackground(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(25)

        # Title
        title = QLabel("Welcome to TodoApp")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(self.TITLE_FONT)
        layout.addWidget(title)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(self.INPUT_HEIGHT)
        add_shadow(self.username_input)
        self.username_input.returnPressed.connect(self.press_button_login)
        layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(self.INPUT_HEIGHT)
        add_shadow(self.password_input)
        self.password_input.returnPressed.connect(self.press_button_login)
        layout.addWidget(self.password_input)

        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setFixedHeight(self.BUTTON_HEIGHT)
        add_shadow(self.login_btn)
        self.login_btn.clicked.connect(self.press_button_login)
        layout.addWidget(self.login_btn)

        # Register + Guest buttons
        row = QHBoxLayout()
        row.setSpacing(20)

        register_btn = QPushButton("Register")
        register_btn.setFixedHeight(self.BUTTON_HEIGHT)
        add_shadow(register_btn)
        register_btn.clicked.connect(self.register_requested.emit)
        row.addWidget(register_btn)

        guest_btn = QPushButton("Continue as Guest")
        guest_btn.setFixedHeight(self.BUTTON_HEIGHT)
        add_shadow(guest_btn)
        guest_btn.clicked.connect(self.guest_requested.emit)
        row.addWidget(guest_btn)

        layout.addLayout(row)
        layout.addStretch()

    def press_button_login(self) ->None:
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if self.validate_inputs(username, password):
            self.login_requested.emit(username, password)
        return None

    def validate_inputs(self, username: str, password: str) -> bool:
        if not username or not password:
            self.notifier.error("Incomplete", "Please fill in both fields.")
            return False
        return True

    def load_styles(self) -> str:
        return """
        QWidget {
            background-color: #121212;
            color: #E0E0E0;
        }
        QLabel {
            color: #BB86FC;
        }
        QLineEdit {
            background-color: #2C2C2C;
            color: #FFFFFF;
            border: 2px solid #3E3E3E;
            border-radius: 20px;
            padding: 12px;
            font-size: 16px;
        }
        QLineEdit:focus {
            border: 2px solid #BB86FC;
            background-color: #1E1E1E;
        }
        QPushButton {
            background-color: #BB86FC;
            border: none;
            border-radius: 20px;
            color: black;
            font-size: 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #9B6DFF;
        }
        QPushButton:pressed {
            background-color: #7F39FB;
        }
        """


def add_shadow(widget) -> None:
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(25)
    shadow.setOffset(0, 5)
    shadow.setColor(QColor(0, 0, 0, 150))
    widget.setGraphicsEffect(shadow)
    return None
