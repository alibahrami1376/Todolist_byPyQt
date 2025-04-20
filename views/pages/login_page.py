from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

class LoginPage(QWidget):
    login_requested = pyqtSignal(str, str)
    register_requested = pyqtSignal()
    guest_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(100, 80, 100, 80)
        layout.setSpacing(20)

        # Title
        title = QLabel("<h1>Welcome to TodoApp</h1>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)
        layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)
        layout.addWidget(self.password_input)

        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)

        # Register and guest buttons
        row = QHBoxLayout()

        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.register_requested.emit)
        row.addWidget(register_btn)

        guest_btn = QPushButton("Continue as Guest")
        guest_btn.clicked.connect(self.guest_requested.emit)
        row.addWidget(guest_btn)

        layout.addLayout(row)
        layout.addStretch()

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        self.login_requested.emit(username, password)
