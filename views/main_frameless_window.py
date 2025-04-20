
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget,QHBoxLayout
from PyQt6.QtCore import Qt


from views.widgets.custom_titlebar import CustomTitleBar
from views.widgets.sidebar import Sidebar


class MainFramelessWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(1000, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
                font-family: Segoe UI;
                font-size: 14px;
            }
        """)

        self.pages = {}
        self.stack = QStackedWidget()

        self.init_ui()

    def init_ui(self):
        wrapper = QVBoxLayout(self)
        wrapper.setContentsMargins(0, 0, 0, 0)
        wrapper.setSpacing(0)

        # Title Bar
        self.title_bar = CustomTitleBar(self)
        wrapper.addWidget(self.title_bar)
        # Sidebar + Page stack
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.switch_requested.connect(self.switch_page)

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.stack)

        wrapper.addLayout(content_layout)

    def add_page(self, widget: QWidget, name: str):
        self.pages[name.lower()] = widget
        self.stack.addWidget(widget)

    def switch_page(self, name: str):
        if name.lower() in self.pages:
            self.stack.setCurrentWidget(self.pages[name.lower()])
        else:
            raise ValueError(f"Page '{name}' not found.")
    