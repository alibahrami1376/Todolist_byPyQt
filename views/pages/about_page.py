from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
                font-family: Segoe UI;
                font-size: 14px;
            }
        """)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # قاب خاکستری در مرکز صفحه
        box = QFrame()
        box.setFixedWidth(600)
        box.setStyleSheet("""
            QFrame {
                background-color: #2d2d30;
                border-radius: 12px;
                padding: 25px;
            }
        """)

        box_layout = QVBoxLayout(box)
        box_layout.setSpacing(20)

        # متن
        label = QLabel(
            "Tempus\n\nHeya! It's the creator of Tempus. I hope you've enjoyed using this app as much as I enjoyed making it.\n\n"
            "I'm a school student and can't earn money LEGALLY. If you like the app, please consider giving it a ⭐ on GitHub!\n\n"
            "You can also open an issue or feature request on GitHub. Your feedback helps a lot!\n\nThanks for using Tempus! 😊"
        )
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setFont(QFont("Segoe UI", 10))
        box_layout.addWidget(label)

        # دکمه‌ها
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        btn_github = QPushButton("GitHub")
        btn_github.setStyleSheet("""
            QPushButton {
                background-color: #00cfe8;
                color: black;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00b4cc;
            }
        """)

        btn_return = QPushButton("Return")
        btn_return.setStyleSheet("""
            QPushButton {
                background-color: #3e3e42;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)

        button_layout.addWidget(btn_github)
        button_layout.addWidget(btn_return)

        box_layout.addLayout(button_layout)
        main_layout.addWidget(box)

        # اتصال عملکرد برگشت
        btn_return.clicked.connect(lambda: self.parent().switch_requested.emit("dashboard"))
