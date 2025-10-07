from PyQt6.QtWidgets import QFrame, QVBoxLayout, QToolButton, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon

class Sidebar(QFrame):
    switch_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.expanded = True
        self.is_dark = True
        self.setFixedWidth(100)  
        # set initial bg; full theming applied after buttons are created
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
            ("Projects", "project.png"),
            ("LearningPaths", "learning.png"),
        ]

        for name, icon in self.sections:
            self.add_button(name, icon)

        self.layout_main.addStretch()

        # Now that buttons exist, apply full theme
        self.apply_theme(self.is_dark)

    def add_button(self, name, icon_file):
        btn = QToolButton()
        btn.setText(name if self.expanded else "")
        btn.setIcon(QIcon(f"icons/{icon_file}"))
        btn.setIconSize(QSize(24, 24))
        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon if self.expanded else Qt.ToolButtonStyle.ToolButtonIconOnly)
        btn.setObjectName(name.lower())
        btn.setCheckable(True)
        btn.setStyleSheet(self.style_button(False, self.is_dark))
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn.clicked.connect(lambda checked, n=name: self.on_click(n))
        self.layout_main.addWidget(btn)
        self.buttons[name] = btn

    def on_click(self, name):
        for btn_name, btn in self.buttons.items():
            btn.setChecked(btn_name == name)
            btn.setStyleSheet(self.style_button(btn.isChecked(), self.is_dark))
        self.switch_requested.emit(name.lower())

    def style_button(self, active, is_dark):
        if is_dark:
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
        else:
            if active:
                return """
                QToolButton {
                    text-align: left;
                    padding-left: 10px;
                    color: #2b59c3;
                    background-color: #e6eaf3;
                    border-left: 4px solid #2b59c3;
                    border-radius: 8px;
                }
                QToolButton:hover {
                    background-color: #dfe7f7;
                }
                """
            else:
                return """
                QToolButton {
                    text-align: left;
                    padding-left: 10px;
                    color: #1e1e1e;
                    background-color: #f4f4f4;
                    border: none;
                    border-radius: 6px;
                }
                QToolButton:hover {
                    background-color: #e9e9e9;
                }
                """


    def toggle(self):
        self.expanded = not self.expanded
        self.setFixedWidth(100 if self.expanded else 50)

        for name, btn in self.buttons.items():
            btn.setText(name if self.expanded else "")
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon if self.expanded else Qt.ToolButtonStyle.ToolButtonIconOnly)

    def apply_theme(self, is_dark: bool):
        self.is_dark = is_dark
        if is_dark:
            self.setStyleSheet("background-color: #2d2d30;")
        else:
            self.setStyleSheet("background-color: #f1f1f1;")
        if not hasattr(self, "buttons"):
            return
        for name, btn in self.buttons.items():
            btn.setStyleSheet(self.style_button(btn.isChecked(), self.is_dark))
