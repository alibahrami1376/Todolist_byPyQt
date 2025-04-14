import sys


from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve


from views.view_pagemanager import PageManagerWindow
from utils.stylesheet_loader import load_stylesheet


USERNAME = "user"
PASSWORD = "pass"


class LoginPage(QWidget):
    def __init__(self,manager: PageManagerWindow):
        super().__init__()
        self.manager = manager
        self.init_ui()
        self.show_animation()


    def init_ui(self):
        
        title = QLabel("Login")
        title.setFont(QFont('Segoe UI', 30, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #BB86FC;")

        self.create_buttons()
        self.create_input_fields()

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(100)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addSpacing(20)
        layout.addLayout(self.button_layout)
        layout.addStretch()
        self.setLayout(layout)


    def create_input_fields(self):

        font = QFont('Segoe UI', 10)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setFont(font)
        self.username.setFixedHeight(40)
        self.username.setObjectName("username")
        self.username.setStyleSheet(load_stylesheet("styles/login/username.qss"))       

        self.username.returnPressed.connect(self.handle_login)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setFont(font)
        self.password.setFixedHeight(40)
        self.password.setObjectName("password")
        self.password.setStyleSheet(load_stylesheet("styles/login/password.qss"))
        self.password.returnPressed.connect(self.handle_login)
        

    def create_buttons(self):
        font_button = QFont('Segoe UI', 10, QFont.Weight.Bold)
        btn_login = QPushButton("login")
        btn_login.setFont(font_button)
        btn_login.setFixedHeight(40)
        btn_login.setStyleSheet(load_stylesheet("styles/login/button_login.qss"))
        # title_lable_btn_login = QLabel("login")
        # title_lable_btn_login.setObjectName("login")

        btn_login.clicked.connect(self.handle_login)

        btn_exit = QPushButton("exit")
        btn_exit.setFont(font_button)
        btn_exit.setFixedHeight(40)
        btn_exit.setStyleSheet(load_stylesheet("styles/login/button_exit.qss"))
        btn_exit.clicked.connect(sys.exit)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(btn_login)
        self.button_layout.addWidget(btn_exit)

        
    def handle_login(self):
        # اعتبارسنجی ساده: در اینجا نام کاربری "user" و رمز "pass" در نظر گرفته شده است.
        username = self.username.text().strip()
        password = self.password.text().strip()
        error = self.validate_login(username, password)
        if error:
            self.show_warning(error)
            return
        self.manager.switch_page("home")


    def show_warning(self, message: str):
        QMessageBox.warning(self, "Warning", message, QMessageBox.StandardButton.Ok)


    def show_animation(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(1500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.start()


    def validate_login(self, username, password):
        if not username or not password:
            return "Please fill in both fields."
        if username != USERNAME or password != PASSWORD:
            return "Incorrect username or password. Please try again."
        return None
