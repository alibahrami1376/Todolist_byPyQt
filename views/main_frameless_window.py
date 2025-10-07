from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QToolButton, QLabel, QToolBar, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, QSize
import os


from views.widgets.custom_titlebar import CustomTitleBar
from views.widgets.sidebar import Sidebar
from views.widgets.custom_menubar import CustomMenuBar
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
        # نوار منو (هدر)
        self.menu_bar = CustomMenuBar(self)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(1000, 600)
        self.apply_theme_from_config()

        self.pages = {}
        self.sidebar_hidden = False
        self.stack = QStackedWidget()

        # ساخت نوار ابزار بالایی
        self.top_toolbar = QToolBar("Top Toolbar", self)
        self.top_toolbar.setIconSize(QSize(18, 18))
        # رنگ نوار ابزار بالایی را با رنگ اپلیکیشن هماهنگ کن
        self.top_toolbar.setStyleSheet("QToolBar { background: none; border: none; }")
        # افزودن دکمه‌ها به نوار بالایی و دکمه جمع‌کننده نوار بغل
        self._add_top_toolbar_actions()
        self._add_sidebar_handle_to_toolbar()
    def _add_sidebar_handle_to_toolbar(self):
        # دکمه جمع‌کننده نوار بغل (≡) را به نوار ابزار بالایی منتقل کن
        self.sidebar_handle = QToolButton()
        self.sidebar_handle.setText("≡")
        self.sidebar_handle.setFixedWidth(24)
        self.sidebar_handle.clicked.connect(self.toggle_sidebar)
        self.sidebar_handle.setToolTip("نمایش/مخفی کردن نوار بغل")
        self.top_toolbar.addWidget(self.sidebar_handle)

        # ساخت نوار ابزار پایینی
        self.bottom_toolbar = QToolBar("Bottom Toolbar", self)
        self.bottom_toolbar.setIconSize(QSize(18, 18))
        self.bottom_toolbar.setFixedHeight(25)
        self.bottom_toolbar.setStyleSheet("QToolBar { background: #222; color: #fff; border: none; }")
        self.bottom_toolbar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self._add_bottom_toolbar_widgets()

        # ...existing code...
        self.init_ui()
    def _add_top_toolbar_actions(self):
        from PyQt6.QtGui import QIcon
        # مسیر آیکون‌ها
        icon_path = lambda name: os.path.join("icons", name)
        # افزودن دکمه افزودن
        add_action = self.top_toolbar.addAction(QIcon(icon_path("add.png")), "افزودن")
        add_action.setToolTip("افزودن مورد جدید")
        # افزودن دکمه ذخیره
        save_action = self.top_toolbar.addAction(QIcon(icon_path("save.png")) if os.path.exists(icon_path("save.png")) else QIcon(icon_path("add.png")), "ذخیره")
        save_action.setToolTip("ذخیره تغییرات")
        # افزودن دکمه به‌روزرسانی
        update_action = self.top_toolbar.addAction(QIcon(icon_path("update.png")) if os.path.exists(icon_path("update.png")) else QIcon(icon_path("add.png")), "به‌روزرسانی")
        update_action.setToolTip("به‌روزرسانی اطلاعات")

    def _add_bottom_toolbar_widgets(self):
        from PyQt6.QtGui import QIcon
        # ساعت
        clock_label = QLabel("12:00")
        clock_label.setStyleSheet("color: #fff; font-size: 13px; margin-left: 8px;")
        self.bottom_toolbar.addWidget(clock_label)
        # وضعیت اتصال
        status_label = QLabel("وضعیت: متصل")
        status_label.setStyleSheet("color: #fff; font-size: 13px; margin-left: 16px;")
        self.bottom_toolbar.addWidget(status_label)
        # پیام‌ها
        msg_icon = QToolButton()
        msg_icon.setIcon(QIcon(os.path.join("icons", "information.png")))
        msg_icon.setIconSize(QSize(16, 16))
        msg_icon.setStyleSheet("background: transparent; margin-left: 16px;")
        msg_icon.setToolTip("پیام‌ها")
        self.bottom_toolbar.addWidget(msg_icon)
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

        # نوار عنوان سفارشی
        self.title_bar = CustomTitleBar(self)
        self.title_bar.setStyleSheet("padding-top: 8px;")
        wrapper.addWidget(self.title_bar)

        # نوار ابزار بالایی
        wrapper.addWidget(self.top_toolbar)

        # محتوای صفحات (QStackedWidget + Sidebar)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.switch_requested.connect(self.switch_page)
        self.sidebar.request_hide.connect(self.toggle_sidebar)
        content_layout.addWidget(self.sidebar)

        content_layout.addWidget(self.stack)

        wrapper.addLayout(content_layout)

        # نوار ابزار پایینی
        wrapper.addWidget(self.bottom_toolbar)

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
        if hasattr(self, "sidebar_handle"):
            self.sidebar_handle.setVisible(self.sidebar_hidden)
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
