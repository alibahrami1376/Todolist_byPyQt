from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QToolButton, QLabel, QToolBar, QSizePolicy, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QPoint
from PyQt6.QtGui import QMouseEvent
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
        self.is_dark_theme = True  # Track theme state

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Enable window resizing
        self.setMinimumSize(600, 400)  # Smaller minimum size for better responsiveness
        self.resize(1000, 650)  # Set initial size
        self.apply_theme_from_config()

        self.pages = {}
        self.sidebar_hidden = False
        self.stack = QStackedWidget()

        # ساخت نوار ابزار بالایی
        self.top_toolbar = QToolBar("Top Toolbar", self)
        self.top_toolbar.setIconSize(QSize(18, 18))
        self.top_toolbar.setMovable(False)  # Prevent toolbar from being moved
        # رنگ نوار ابزار بالایی را با رنگ اپلیکیشن هماهنگ کن
        self.top_toolbar.setStyleSheet("QToolBar { background: none; border: none; padding: 0px; }")
        # افزودن دکمه‌ها به نوار بالایی و دکمه جمع‌کننده نوار بغل
        self._add_top_toolbar_actions()
        self._add_sidebar_handle_to_toolbar()
    def _add_sidebar_handle_to_toolbar(self):


        # ساخت نوار ابزار پایینی
        self.bottom_toolbar = QToolBar("Bottom Toolbar", self)
        self.bottom_toolbar.setIconSize(QSize(18, 18))
        self.bottom_toolbar.setFixedHeight(25)
        self.bottom_toolbar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self._add_bottom_toolbar_widgets()

        # ...existing code...
        self.init_ui()
    def _add_top_toolbar_actions(self):
        from PyQt6.QtGui import QIcon
        from PyQt6.QtWidgets import QToolButton, QWidget, QHBoxLayout, QSizePolicy
        icon_path = lambda name: os.path.join("icons", name)

        # ساخت ویجت مرکزی برای چیدمان دکمه‌ها
        toolbar_widget = QWidget()
        layout = QHBoxLayout(toolbar_widget)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        # دکمه افزودن
        self.btn_add = QToolButton()
        self.btn_add.setIcon(QIcon(icon_path("add.png")))
        self.btn_add.setIconSize(QSize(18, 18))
        self.btn_add.setToolTip("افزودن مورد جدید")
        layout.addWidget(self.btn_add)

        # دکمه ذخیره
        self.btn_save = QToolButton()
        self.btn_save.setIcon(QIcon(icon_path("save.png")) if os.path.exists(icon_path("save.png")) else QIcon(icon_path("add.png")))
        self.btn_save.setIconSize(QSize(18, 18))
        self.btn_save.setToolTip("ذخیره تغییرات")
        layout.addWidget(self.btn_save)

        # دکمه به‌روزرسانی
        self.btn_update = QToolButton()
        self.btn_update.setIcon(QIcon(icon_path("update.png")) if os.path.exists(icon_path("update.png")) else QIcon(icon_path("add.png")))
        self.btn_update.setIconSize(QSize(18, 18))
        self.btn_update.setToolTip("به‌روزرسانی اطلاعات")
        layout.addWidget(self.btn_update)

        # separator
        sep = QWidget()
        sep.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(sep)

        # دکمه جمع‌کننده نوار بغل (≡)
        self.sidebar_handle = QToolButton()
        self.sidebar_handle.setText("≡")
        self.sidebar_handle.setFixedWidth(28)
        self.sidebar_handle.setToolTip("نمایش/مخفی کردن نوار بغل")
        self.sidebar_handle.clicked.connect(self.toggle_sidebar)
        layout.addWidget(self.sidebar_handle)

        self.top_toolbar.addWidget(toolbar_widget)
        # Apply theme after widgets are created
        self._apply_toolbar_theme()

    def _add_bottom_toolbar_widgets(self):
        from PyQt6.QtGui import QIcon
        # ساعت
        self.clock_label = QLabel("12:00")
        self.clock_label.setStyleSheet("font-size: 13px; margin-left: 8px;")
        self.bottom_toolbar.addWidget(self.clock_label)
        # وضعیت اتصال
        self.status_label = QLabel("وضعیت: متصل")
        self.status_label.setStyleSheet("font-size: 13px; margin-left: 16px;")
        self.bottom_toolbar.addWidget(self.status_label)
        # پیام‌ها
        self.msg_icon = QToolButton()
        self.msg_icon.setIcon(QIcon(os.path.join("icons", "information.png")))
        self.msg_icon.setIconSize(QSize(16, 16))
        self.msg_icon.setStyleSheet("background: transparent; margin-left: 16px;")
        self.msg_icon.setToolTip("پیام‌ها")
        self.bottom_toolbar.addWidget(self.msg_icon)
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
            self.is_dark_theme = True
            self.setStyleSheet(load_stylesheet("styles/dark.qss"))
            # propagate to composed widgets
            # title bar & sidebar have their own palette; sync them
            if hasattr(self, "title_bar"):
                self.title_bar.apply_theme(True)
            if hasattr(self, "sidebar"):
                self.sidebar.apply_theme(True)
        else:
            self.is_dark_theme = False
            self.setStyleSheet(load_stylesheet("styles/light.qss"))
            if hasattr(self, "title_bar"):
                self.title_bar.apply_theme(False)
            if hasattr(self, "sidebar"):
                self.sidebar.apply_theme(False)
        
        # Apply toolbar themes if widgets exist
        if hasattr(self, "top_toolbar"):
            self._apply_toolbar_theme()
    
    def _apply_toolbar_theme(self):
        """Apply theme to toolbar buttons and bottom toolbar"""
        if self.is_dark_theme:
            # Dark theme styles
            toolbar_button_style = """
                QToolButton {
                    background-color: #444444;
                    color: white;
                    border-radius: 5px;
                    padding: 4px 10px;
                }
                QToolButton:hover {
                    background-color: #555555;
                }
                QToolButton:pressed {
                    background-color: #666666;
                }
            """
            bottom_toolbar_style = "QToolBar { background-color: #2d2d30; color: white; border: none; }"
            label_color = "color: white;"
        else:
            # Light theme styles
            toolbar_button_style = """
                QToolButton {
                    background-color: #eaeaea;
                    color: #1e1e1e;
                    border-radius: 5px;
                    padding: 4px 10px;
                }
                QToolButton:hover {
                    background-color: #dcdcdc;
                }
                QToolButton:pressed {
                    background-color: #c0c0c0;
                }
            """
            bottom_toolbar_style = "QToolBar { background-color: #f1f1f1; color: #1e1e1e; border-top: 1px solid #ddd; border: none; }"
            label_color = "color: #1e1e1e;"
        
        # Apply to top toolbar buttons
        if hasattr(self, "btn_add"):
            self.btn_add.setStyleSheet(toolbar_button_style)
        if hasattr(self, "btn_save"):
            self.btn_save.setStyleSheet(toolbar_button_style)
        if hasattr(self, "btn_update"):
            self.btn_update.setStyleSheet(toolbar_button_style)
        if hasattr(self, "sidebar_handle"):
            self.sidebar_handle.setStyleSheet(toolbar_button_style + " font-size: 18px;")
        
        # Apply to bottom toolbar
        if hasattr(self, "bottom_toolbar"):
            self.bottom_toolbar.setStyleSheet(bottom_toolbar_style)
        if hasattr(self, "clock_label"):
            self.clock_label.setStyleSheet(label_color + " font-size: 13px; margin-left: 8px;")
        if hasattr(self, "status_label"):
            self.status_label.setStyleSheet(label_color + " font-size: 13px; margin-left: 16px;")

    def init_ui(self):
        wrapper = QVBoxLayout(self)
        wrapper.setContentsMargins(0, 0, 0, 0)
        wrapper.setSpacing(0)

        # نوار عنوان سفارشی
        self.title_bar = CustomTitleBar(self)
        wrapper.addWidget(self.title_bar)

        # نوار ابزار بالایی
        self.top_toolbar.setFixedHeight(35)  # Set fixed height to reduce spacing
        wrapper.addWidget(self.top_toolbar)

        # محتوای صفحات (QStackedWidget + Sidebar)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.switch_requested.connect(self.switch_page)
        self.sidebar.request_hide.connect(self.toggle_sidebar)
        content_layout.addWidget(self.sidebar)

        # Wrap stack in scroll area for responsive pages
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.stack)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        content_layout.addWidget(scroll_area)

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
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for window resizing"""
        # Don't interfere with title bar dragging
        if hasattr(self, 'title_bar') and self.title_bar.geometry().contains(event.position().toPoint()):
            return
        
        if event.button() == Qt.MouseButton.LeftButton:
            self._resize_start_pos = event.globalPosition().toPoint()
            self._resize_start_geometry = self.geometry()
            # Check if mouse is near edges for resizing
            edge_margin = 5
            pos = event.position().toPoint()
            width = self.width()
            height = self.height()
            
            # Determine resize direction
            self._resize_direction = 0
            if pos.x() <= edge_margin:
                self._resize_direction |= 1  # Left
            if pos.x() >= width - edge_margin:
                self._resize_direction |= 2  # Right
            if pos.y() <= edge_margin:
                self._resize_direction |= 4  # Top
            if pos.y() >= height - edge_margin:
                self._resize_direction |= 8  # Bottom
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move for window resizing"""
        if not hasattr(self, '_resize_start_pos') or self._resize_start_pos is None:
            return
        
        if not hasattr(self, '_resize_direction') or self._resize_direction == 0:
            return
        
        current_pos = event.globalPosition().toPoint()
        delta = current_pos - self._resize_start_pos
        
        x = self._resize_start_geometry.x()
        y = self._resize_start_geometry.y()
        width = self._resize_start_geometry.width()
        height = self._resize_start_geometry.height()
        
        # Apply resize based on direction
        if self._resize_direction & 1:  # Left
            x += delta.x()
            width -= delta.x()
        if self._resize_direction & 2:  # Right
            width += delta.x()
        if self._resize_direction & 4:  # Top
            y += delta.y()
            height -= delta.y()
        if self._resize_direction & 8:  # Bottom
            height += delta.y()
        
        # Ensure minimum size
        min_width = self.minimumWidth()
        min_height = self.minimumHeight()
        
        if width < min_width:
            if self._resize_direction & 1:
                x -= (min_width - width)
            width = min_width
        if height < min_height:
            if self._resize_direction & 4:
                y -= (min_height - height)
            height = min_height
        
        self.setGeometry(x, y, width, height)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Reset resize state on mouse release"""
        if hasattr(self, '_resize_start_pos'):
            self._resize_start_pos = None
        if hasattr(self, '_resize_direction'):
            self._resize_direction = 0
    
    def changeEvent(self, event):
        """Update cursor when entering/leaving resize areas"""
        super().changeEvent(event)
        # This will be handled by checking cursor position in real-time
