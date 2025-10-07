
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout
from PyQt6.QtCore import Qt,pyqtSignal
import os


from views.widgets.custom_titlebar import CustomTitleBar
from views.widgets.sidebar import Sidebar
from utils.app_notifier import AppNotifier
from core.session_manager import Session
from views.pages.theme_settings_page import ThemeSettingsPage
from utils.stylesheet_loader import load_stylesheet

class MainFramelessWindow(QWidget):
    handle_exit= pyqtSignal()
    def __init__(self):
        super().__init__()
        
        self.notifier = AppNotifier(self)
        self.notifier.set_parent(self)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(1000, 600)
        self.apply_theme_from_config()

        self.pages = {}
        self.sidebar_hidden = False
        self.stack = QStackedWidget()
        self.init_ui()
    # افزودن صفحه تنظیمات تم
        self.theme_settings_page = ThemeSettingsPage(main_window=self)
        self.add_page(self.theme_settings_page, "تنظیمات تم")

    def apply_theme_from_config(self):
        config_path = "configg/theme_config.txt"
        theme = "روشن"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    theme = f.read().strip() or "روشن"
            except Exception:
                theme = "روشن"

        if theme == "دارک":
            self.setStyleSheet(load_stylesheet("styles/dark.qss"))
            # propagate to composed widgets
            # title bar & sidebar have their own palette; sync them
            if hasattr(self, "title_bar"):
                self.title_bar.apply_theme(True)
            if hasattr(self, "sidebar"):
                self.sidebar.apply_theme(True)
        else:
            self.setStyleSheet(load_stylesheet("styles/light.qss"))
            if hasattr(self, "title_bar"):
                self.title_bar.apply_theme(False)
            if hasattr(self, "sidebar"):
                self.sidebar.apply_theme(False)

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

    def toggle_sidebar(self):
        if not hasattr(self, "sidebar"):
            return
        self.sidebar_hidden = not self.sidebar_hidden
        self.sidebar.setVisible(not self.sidebar_hidden)
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
        