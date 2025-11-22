from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, QPoint, QSize
import os
import math
from utils.stylesheet_loader import load_stylesheet
from PyQt6.QtGui import QIcon, QPainter, QPen, QBrush, QColor, QPixmap

class CustomTitleBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(35)
        self.is_dark = True
        self.old_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(5)

        # App icon (optional)
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QIcon("images/checklist.png").pixmap(20, 20))
        layout.addWidget(self.icon_label)

        # Title text
        self.title_label = QLabel("  My Application")
        self.title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.title_label)
        layout.addStretch()

        # Minimize button
        self.minimize_btn = QPushButton()
        self.minimize_btn.setIcon(self._create_minimize_icon())
        self.minimize_btn.setIconSize(QSize(16, 16))
        self.minimize_btn.setFixedSize(32, 32)
        self.minimize_btn.setToolTip("Minimize")
        self.minimize_btn.clicked.connect(self.minimize_window)

        # Close button
        self.close_btn = QPushButton()
        self.close_btn.setIcon(self._create_close_icon())
        self.close_btn.setIconSize(QSize(16, 16))
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.setToolTip("Close")
        self.close_btn.clicked.connect(self.close_window)

        # Sidebar toggle button
        self.sidebar_btn = QPushButton()
        self.sidebar_btn.setIcon(self._create_menu_icon())
        self.sidebar_btn.setIconSize(QSize(18, 18))
        self.sidebar_btn.setFixedSize(32, 32)
        self.sidebar_btn.setToolTip("Toggle Sidebar")
        self.sidebar_btn.clicked.connect(self.toggle_sidebar)

        # Theme toggle button
        self.theme_btn = QPushButton()
        self.theme_btn.setIcon(self._create_theme_icon())
        self.theme_btn.setIconSize(QSize(18, 18))
        self.theme_btn.setFixedSize(32, 32)
        self.theme_btn.setToolTip("Toggle Theme")
        self.theme_btn.clicked.connect(self.toggle_theme)

        for btn in [self.sidebar_btn, self.theme_btn, self.minimize_btn, self.close_btn]:
            btn.setStyleSheet(self.button_style(self.is_dark))
            layout.addWidget(btn)

        # Apply theme after all widgets are created
        self.apply_theme(self.is_dark)

    def minimize_window(self):
        if self.parent:
            self.parent.showMinimized()

    def close_window(self):
        if self.parent:
            self.parent.close()

    def toggle_theme(self):
        if not self.parent:
            return
        # Read current
        config_path = "configg/theme_config.txt"
        current = "روشن"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    current = f.read().strip() or "روشن"
            except Exception:
                current = "روشن"

        new_theme = "دارک" if current != "دارک" else "روشن"
        try:
            os.makedirs("configg", exist_ok=True)
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(new_theme)
        except Exception:
            pass

        if new_theme == "دارک":
            self.parent.is_dark_theme = True
            self.parent.setStyleSheet(load_stylesheet("styles/dark.qss"))
            self.apply_theme(True)
            if hasattr(self.parent, "sidebar"):
                self.parent.sidebar.apply_theme(True)
        else:
            self.parent.is_dark_theme = False
            self.parent.setStyleSheet(load_stylesheet("styles/light.qss"))
            self.apply_theme(False)
            if hasattr(self.parent, "sidebar"):
                self.parent.sidebar.apply_theme(False)
        
        # Update toolbar themes
        if hasattr(self.parent, "_apply_toolbar_theme"):
            self.parent._apply_toolbar_theme()

    def apply_theme(self, is_dark: bool):
        self.is_dark = is_dark
        if is_dark:
            self.setStyleSheet("background-color: #2d2d30;")
            self.title_label.setStyleSheet("font-weight: bold; color: white;")
        else:
            self.setStyleSheet("background-color: #f1f1f1;")
            self.title_label.setStyleSheet("font-weight: bold; color: #1e1e1e;")
        for btn in [self.sidebar_btn, self.theme_btn, self.minimize_btn, self.close_btn]:
            btn.setStyleSheet(self.button_style(is_dark))
        # Update icons with new theme colors
        self.minimize_btn.setIcon(self._create_minimize_icon())
        self.close_btn.setIcon(self._create_close_icon())
        self.sidebar_btn.setIcon(self._create_menu_icon())
        self.theme_btn.setIcon(self._create_theme_icon())

    def button_style(self, is_dark: bool) -> str:
        if is_dark:
            return """
                QPushButton {
                    background-color: transparent;
                    color: white;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #ff5f56;
                    border-radius: 10px;
                }
            """
        return """
            QPushButton {
                background-color: transparent;
                color: #1e1e1e;
                border: none;
            }
            QPushButton:hover {
                background-color: #ffdada;
                border-radius: 10px;
            }
        """

    def toggle_sidebar(self):
        if self.parent:
            if hasattr(self.parent, "toggle_sidebar"):
                self.parent.toggle_sidebar()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return
        delta = event.globalPosition().toPoint() - self.old_pos
        self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()
    
    def _create_minimize_icon(self) -> QIcon:
        """Create minimize icon"""
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor("white") if self.is_dark else QColor("#1e1e1e")
        pen = QPen(color, 2)
        painter.setPen(pen)
        # Draw horizontal line
        painter.drawLine(4, 8, 12, 8)
        painter.end()
        return QIcon(pixmap)
    
    def _create_close_icon(self) -> QIcon:
        """Create close (X) icon"""
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor("white") if self.is_dark else QColor("#1e1e1e")
        pen = QPen(color, 2)
        painter.setPen(pen)
        # Draw X
        painter.drawLine(5, 5, 11, 11)
        painter.drawLine(11, 5, 5, 11)
        painter.end()
        return QIcon(pixmap)
    
    def _create_menu_icon(self) -> QIcon:
        """Create menu/hamburger icon"""
        pixmap = QPixmap(18, 18)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor("white") if self.is_dark else QColor("#1e1e1e")
        pen = QPen(color, 2)
        painter.setPen(pen)
        # Draw three horizontal lines
        painter.drawLine(4, 5, 14, 5)
        painter.drawLine(4, 9, 14, 9)
        painter.drawLine(4, 13, 14, 13)
        painter.end()
        return QIcon(pixmap)
    
    def _create_theme_icon(self) -> QIcon:
        """Create theme toggle icon (sun/moon)"""
        pixmap = QPixmap(18, 18)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor("white") if self.is_dark else QColor("#1e1e1e")
        pen = QPen(color, 1.5)
        painter.setPen(pen)
        
        if self.is_dark:
            # Draw moon icon for dark theme
            painter.drawArc(6, 4, 8, 8, 45 * 16, 180 * 16)
            painter.drawArc(8, 6, 6, 6, 45 * 16, 180 * 16)
        else:
            # Draw sun icon for light theme
            center_x, center_y = 9, 9
            radius = 5
            # Draw circle
            painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
            # Draw rays
            for i in range(8):
                angle = i * 45
                rad = math.radians(angle)
                x1 = center_x + (radius + 2) * math.cos(rad)
                y1 = center_y + (radius + 2) * math.sin(rad)
                x2 = center_x + (radius + 4) * math.cos(rad)
                y2 = center_y + (radius + 4) * math.sin(rad)
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
        
        painter.end()
        return QIcon(pixmap)
