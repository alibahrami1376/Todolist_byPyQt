# تنظیمات تم (دارک و روشن) برای پروژه PyQt
# این فایل یک صفحه تنظیمات پیشرفته برای انتخاب و ذخیره تم را فراهم می‌کند.

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt6.QtCore import Qt
import os

class ThemeSettingsPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        self.load_theme()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        label = QLabel("انتخاب تم برنامه:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["روشن", "دارک"])
        layout.addWidget(self.theme_selector)

        self.save_btn = QPushButton("ذخیره تنظیمات")
        self.save_btn.clicked.connect(self.save_theme)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def save_theme(self):
        theme = self.theme_selector.currentText()
        with open("configg/theme_config.txt", "w", encoding="utf-8") as f:
            f.write(theme)
        self.apply_theme(theme)

    def load_theme(self):
        theme = "روشن"
        config_path = "configg/theme_config.txt"
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                theme = f.read().strip()
        self.theme_selector.setCurrentText(theme)
        self.apply_theme(theme)

    def apply_theme(self, theme):
        if self.main_window:
            if theme == "دارک":
                self.main_window.setStyleSheet(self.load_stylesheet("styles/dark.qss"))
            else:
                self.main_window.setStyleSheet("")

    def load_stylesheet(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""
        
