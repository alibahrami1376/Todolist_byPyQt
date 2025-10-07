from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, QPoint
import os
from utils.stylesheet_loader import load_stylesheet
from PyQt6.QtGui import QIcon

class CustomTitleBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(35)
        self.setStyleSheet("background-color: #2d2d30;")
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
        self.title_label.setStyleSheet("font-weight: bold; color: white;")
        layout.addWidget(self.title_label)
        layout.addStretch()

        # Minimize button
        self.minimize_btn = QPushButton("–")
        self.minimize_btn.setFixedSize(20, 20)
        self.minimize_btn.clicked.connect(self.minimize_window)

        # Close button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.clicked.connect(self.close_window)

        # Theme toggle button
        self.theme_btn = QPushButton("☼")
        self.theme_btn.setFixedSize(24, 24)
        self.theme_btn.clicked.connect(self.toggle_theme)

        for btn in [self.theme_btn, self.minimize_btn, self.close_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #ff5f56;
                    border-radius: 10px;
                }
            """)
            layout.addWidget(btn)

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
            self.parent.setStyleSheet(load_stylesheet("styles/dark.qss"))
        else:
            self.parent.setStyleSheet("")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return
        delta = event.globalPosition().toPoint() - self.old_pos
        self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()
