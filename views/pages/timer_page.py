from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QPainter, QColor, QPen
import math

class TimerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
                font-family: Segoe UI;
            }
            QPushButton {
                background-color: #3e3e42;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #0078d7;
            }
            QComboBox {
                background-color: #3e3e42;
                color: white;
                padding: 6px;
                border-radius: 4px;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Pomodoro (25 min)", "Short Break (5 min)", "Long Break (15 min)"])
        self.mode_selector.currentIndexChanged.connect(self.change_mode)
        layout.addWidget(self.mode_selector)

        self.time_label = QLabel("25:00")
        self.time_label.setFont(QFont("Segoe UI", 48, QFont.Weight.Bold))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)

        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.pause_btn = QPushButton("Pause")
        self.reset_btn = QPushButton("Reset")

        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.reset_btn.clicked.connect(self.reset_timer)

        for btn in [self.start_btn, self.pause_btn, self.reset_btn]:
            btn.setFixedWidth(100)
            button_layout.addWidget(btn)

        layout.addLayout(button_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.total_seconds = 25 * 60
        self.remaining_seconds = self.total_seconds

    def change_mode(self, index):
        if index == 0:
            self.total_seconds = 25 * 60
        elif index == 1:
            self.total_seconds = 5 * 60
        elif index == 2:
            self.total_seconds = 15 * 60
        self.reset_timer()

    def start_timer(self):
        self.timer.start(1000)

    def pause_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.remaining_seconds = self.total_seconds
        self.update_time_display()
        self.update()

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_time_display()
            self.update()
        else:
            self.timer.stop()
            self.play_alarm()

    def update_time_display(self):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

    def play_alarm(self):
        # TODO: پخش صدا یا نمایش پیام پایان تایمر
        print("Timer finished!")

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect().adjusted(10, 10, -10, -10)

        pen = QPen(QColor("#0078d7"))
        pen.setWidth(10)
        painter.setPen(pen)

        angle = 360 * (1 - self.remaining_seconds / self.total_seconds)
        painter.drawArc(rect, 90 * 16, -int(angle * 16))  

        painter.end()
