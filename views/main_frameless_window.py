from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QToolButton, QLabel, QToolBar, QSizePolicy, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QPoint
from PyQt6.QtGui import QMouseEvent, QCursor
import os


from views.widgets.custom_titlebar import CustomTitleBar
from views.widgets.sidebar import Sidebar
from views.widgets.custom_menubar import CustomMenuBar
from utils.app_notifier import AppNotifier
from core.session_manager import Session
from views.pages.theme_settings_page import ThemeSettingsPage
from utils.stylesheet_loader import load_stylesheet
from utils.app_config import AppConfig

class MainFramelessWindow(QWidget):
    
    handle_exit= pyqtSignal()
    def __init__(self):
        super().__init__()
        # Initialize resize state variables early to avoid AttributeError
        self._resize_start_pos = None
        self._resize_direction = 0
        
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
        self._add_bottom_toolbar()

    def _add_sidebar_handle_to_toolbar(self):
        # این تابع در حال حاضر خالی است چون دکمه sidebar_handle
        # در _add_top_toolbar_actions() ساخته می‌شود
        # می‌توانید این تابع را حذف کنید یا کدهای مرتبط را اینجا منتقل کنید
        pass

    def _add_bottom_toolbar(self):
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

        # دکمه جمع‌کننده نوار بغل
        self.sidebar_handle = QToolButton()
        # استفاده از آیکون به جای متن
        sidebar_icon_path = icon_path("more.png")
        if os.path.exists(sidebar_icon_path):
            self.sidebar_handle.setIcon(QIcon(sidebar_icon_path))
        else:
            # اگر آیکون موجود نبود، از متن استفاده می‌شود
            self.sidebar_handle.setText("≡")
        self.sidebar_handle.setIconSize(QSize(18, 18))
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
        # بارگذاری تم از دیتابیس
        theme = AppConfig.get_theme()

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
            # Dark theme styles inspired by VS Code
            toolbar_button_style = """
                QToolButton {
                    background-color: #252526;
                    color: #d7dae0;
                    border-radius: 8px;
                    padding: 4px 12px;
                    border: 1px solid #3c3c3c;
                }
                QToolButton:hover {
                    background-color: #2f2f37;
                    border-color: #569cd6;
                }
                QToolButton:pressed {
                    background-color: #0e639c;
                    border-color: #0e639c;
                    color: #ffffff;
                }
            """
            bottom_toolbar_style = (
                "QToolBar { background-color: #1b1f2b; color: #d7dae0; border-top: 1px solid #262b3c; }"
            )
            label_color = "color: #cfd6e5;"
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
            # اگر آیکون دارد، استایل عادی را اعمال کن، در غیر این صورت فونت بزرگتر برای متن
            if self.sidebar_handle.icon().isNull():
                self.sidebar_handle.setStyleSheet(toolbar_button_style + " font-size: 18px;")
            else:
                self.sidebar_handle.setStyleSheet(toolbar_button_style)
        
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
        
        # تنظیم وضعیت اولیه: sidebar نمایش داده می‌شود، پس handle مخفی است
        if hasattr(self, "sidebar_handle"):
            self.sidebar_handle.setVisible(False)

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
        name_lower = name.lower()
        if name_lower in self.pages:
            self.stack.setCurrentWidget(self.pages[name_lower])
        else:
            print(f"Warning: Page '{name}' (as '{name_lower}') not found in pages. Available pages: {list(self.pages.keys())}")
            raise ValueError(f"Page '{name}' not found. Available pages: {list(self.pages.keys())}")

    def toggle_sidebar(self):
        if not hasattr(self, "sidebar"):
            return
        self.sidebar_hidden = not self.sidebar_hidden
        # اگر sidebar مخفی است، آن را مخفی کن و دکمه handle را نمایش بده
        # اگر sidebar نمایش داده می‌شود، آن را نمایش بده و دکمه handle را مخفی کن
        self.sidebar.setVisible(not self.sidebar_hidden)
        if hasattr(self, "sidebar_handle"):
            # دکمه handle فقط زمانی نمایش داده می‌شود که sidebar مخفی باشد
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
    
    def _get_resize_direction(self, pos: QPoint) -> int:
        """Get resize direction based on mouse position"""
        edge_margin = 5
        width = self.width()
        height = self.height()
        
        direction = 0
        if pos.x() <= edge_margin:
            direction |= 1  # Left
        if pos.x() >= width - edge_margin:
            direction |= 2  # Right
        if pos.y() <= edge_margin:
            direction |= 4  # Top
        if pos.y() >= height - edge_margin:
            direction |= 8  # Bottom
        
        return direction
    
    def _update_cursor(self, pos: QPoint):
        """Update cursor based on mouse position - optimized to avoid unnecessary updates"""
        # Don't change cursor if over title bar
        if hasattr(self, 'title_bar') and self.title_bar.geometry().contains(pos):
            current_cursor = self.cursor().shape()
            if current_cursor != Qt.CursorShape.ArrowCursor:
                self.setCursor(Qt.CursorShape.ArrowCursor)
            return
        
        direction = self._get_resize_direction(pos)
        
        # Map direction to cursor shape
        cursor_map = {
            0: Qt.CursorShape.ArrowCursor,
            1: Qt.CursorShape.SizeHorCursor,  # Left
            2: Qt.CursorShape.SizeHorCursor,  # Right
            4: Qt.CursorShape.SizeVerCursor,  # Top
            5: Qt.CursorShape.SizeFDiagCursor,  # Top-Left
            6: Qt.CursorShape.SizeBDiagCursor,  # Top-Right
            8: Qt.CursorShape.SizeVerCursor,  # Bottom
            9: Qt.CursorShape.SizeBDiagCursor,  # Bottom-Left
            10: Qt.CursorShape.SizeFDiagCursor,  # Bottom-Right
        }
        
        new_cursor = cursor_map.get(direction, Qt.CursorShape.ArrowCursor)
        current_cursor = self.cursor().shape()
        if current_cursor != new_cursor:
            self.setCursor(new_cursor)
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for window resizing"""
        # Don't interfere with title bar dragging
        if hasattr(self, 'title_bar') and self.title_bar.geometry().contains(event.position().toPoint()):
            return
        
        if event.button() == Qt.MouseButton.LeftButton:
            self._resize_start_pos = event.globalPosition().toPoint()
            self._resize_start_geometry = self.geometry()
            # Get resize direction
            self._resize_direction = self._get_resize_direction(event.position().toPoint())
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move for window resizing"""
        pos = event.position().toPoint()
        
        # Check if we're currently resizing
        is_resizing = self._resize_start_pos is not None
        
        # Update cursor if not resizing
        if not is_resizing:
            self._update_cursor(pos)
            return
        
        # Handle resizing
        if self._resize_direction == 0:
            self._update_cursor(pos)
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
        self._resize_start_pos = None
        self._resize_direction = 0
        # Update cursor after release
        self._update_cursor(event.position().toPoint())
    
    def leaveEvent(self, event):
        """Reset cursor when mouse leaves window"""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)
