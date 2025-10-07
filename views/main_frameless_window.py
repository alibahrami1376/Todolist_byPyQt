
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout
from PyQt6.QtCore import Qt,pyqtSignal


from views.widgets.custom_titlebar import CustomTitleBar
from views.widgets.sidebar import Sidebar
from utils.app_notifier import AppNotifier
from core.session_manager import Session
from views.pages.theme_settings_page import ThemeSettingsPage

class MainFramelessWindow(QWidget):
    handle_exit= pyqtSignal()
    def __init__(self):
        super().__init__()
        
        self.notifier = AppNotifier(self)
        self.notifier.set_parent(self)

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
    # افزودن صفحه تنظیمات تم
        self.theme_settings_page = ThemeSettingsPage(main_window=self)
        self.add_page(self.theme_settings_page, "تنظیمات تم")

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


    def change_page(self,widget_new: QWidget,name: str): 
        self.pages[name.lower()]= widget_new
        self.stack.addWidget(widget_new)
        self.stack.setCurrentWidget(widget_new)


    def switch_page(self, name: str):
        if name.lower() in self.pages:
            self.stack.setCurrentWidget(self.pages[name.lower()])
        else:
            raise ValueError(f"Page '{name}' not found.")
    def closeEvent(self, event):
        if AppNotifier(QWidget).confirm(
            "Exit Confirmation",
            "Are you sure you want to exit? "):
            if Session.is_guest():
               if AppNotifier(QWidget).confirm(
                "save Changes",
                "What if the changes you made to the task are saved?"):
                    self.handle_exit.emit()
            event.accept()
        else:
            event.ignore()
        