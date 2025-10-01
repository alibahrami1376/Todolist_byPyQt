from PyQt6.QtWidgets import QFrame, QVBoxLayout, QToolButton, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon

class Sidebar(QFrame):
    switch_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.expanded = True
        self.setFixedWidth(100)  
        self.setStyleSheet("background-color: #2d2d30;")

        self.layout_main = QVBoxLayout(self)
        self.layout_main.setContentsMargins(5, 10, 5, 10)
        self.layout_main.setSpacing(15)
        self.buttons = {}

        self.sections = [
            ("Dashboard", "dashboard.png"),
            ("Calendar", "calendar.png"),
            ("Journal", "journal.png"),
            ("Timer", "timer.png"),
            ("TodoList", "todolist.png"),
            ("Settings", "settings.png"),
            ("Login", "login.png"),
            ("About", "about.png"),
            ("Fields", "information.png"),
            ("Ideas", "information.png"),
        ]

        for name, icon in self.sections:
            self.add_button(name, icon)

        self.layout_main.addStretch()

    def add_button(self, name, icon_file):
        btn = QToolButton()
        btn.setText(name if self.expanded else "")
        btn.setIcon(QIcon(f"icons/{icon_file}"))
        btn.setIconSize(QSize(24, 24))
        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon if self.expanded else Qt.ToolButtonStyle.ToolButtonIconOnly)
        btn.setObjectName(name.lower())
        btn.setCheckable(True)
        btn.setStyleSheet(self.style_button(False))
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn.clicked.connect(lambda checked, n=name: self.on_click(n))
        self.layout_main.addWidget(btn)
        self.buttons[name] = btn

    def on_click(self, name):
        for btn_name, btn in self.buttons.items():
            btn.setChecked(btn_name == name)
            btn.setStyleSheet(self.style_button(btn.isChecked()))
        self.switch_requested.emit(name.lower())

    def style_button(self, active):
        if active:
            return """
            QToolButton {
                text-align: left;
                padding-left: 10px;
                color: #BB86FC;
                background-color: #3e3e42;
                border-left: 4px solid #BB86FC;
                border-radius: 8px;
            }
            QToolButton:hover {
                background-color: #505050;
            }
            """
        else:
            return """
            QToolButton {
                text-align: left;
                padding-left: 10px;
                color: white;
                background-color: #2d2d30;
                border: none;
                border-radius: 6px;
            }
            QToolButton:hover {
                background-color: #3e3e42;
            }
            """


    def toggle(self):
        self.expanded = not self.expanded
        self.setFixedWidth(100 if self.expanded else 50)

        for name, btn in self.buttons.items():
            btn.setText(name if self.expanded else "")
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon if self.expanded else Qt.ToolButtonStyle.ToolButtonIconOnly)
