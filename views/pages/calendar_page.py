from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCalendarWidget, QFrame
from PyQt6.QtCore import QDate

class CalendarPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header = QLabel("<h2>📆 Calendar</h2>")
        layout.addWidget(header)

        calendar_frame = QFrame()
        calendar_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d30;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        calendar_layout = QVBoxLayout(calendar_frame)
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #1e1e1e;
                color: white;
                border: none;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #0078d7;
                background-color: #2d2d30;
                color: white;
            }
        """)
        self.calendar.setSelectedDate(QDate.currentDate())
        calendar_layout.addWidget(self.calendar)

        layout.addWidget(calendar_frame)
        layout.addStretch()
