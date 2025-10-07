from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class FieldsPage(QWidget):
    def __init__(self, open_field_one, open_field_two, open_field_three, open_field_four):
        super().__init__()
        self.open_field_one = open_field_one
        self.open_field_two = open_field_two
        self.open_field_three = open_field_three
        self.open_field_four = open_field_four

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title = QLabel("Fields Launcher")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(title)

        btn1 = QPushButton("exercise")
        btn1.clicked.connect(self.open_field_one)
        layout.addWidget(btn1)

        btn2 = QPushButton("Nutrition")
        btn2.clicked.connect(self.open_field_two)
        layout.addWidget(btn2)

        btn3 = QPushButton("Programming")
        btn3.clicked.connect(self.open_field_three)
        layout.addWidget(btn3)

        btn4 = QPushButton("English")
        btn4.clicked.connect(self.open_field_four)
        layout.addWidget(btn4)


