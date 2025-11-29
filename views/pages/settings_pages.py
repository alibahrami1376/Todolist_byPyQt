from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QComboBox, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from utils.app_config import AppConfig

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        layout.addWidget(QLabel("<h2>⚙️ Settings</h2>"))

        # Theme toggle
        self.theme_checkbox = QCheckBox("Enable dark theme")
        layout.addWidget(self.build_group("Appearance", [self.theme_checkbox]))

        # Language selector
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "فارسی", "Français"])
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Language:"))
        lang_layout.addWidget(self.language_combo)
        lang_widget = QWidget()
        lang_widget.setLayout(lang_layout)
        layout.addWidget(self.build_group("Language", [lang_widget]))

        # Notification toggle
        self.notify_checkbox = QCheckBox("Enable reminders and task notifications")
        layout.addWidget(self.build_group("Notifications", [self.notify_checkbox]))

        # Save settings button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005fa1;
            }
        """)
        layout.addWidget(self.save_button)
        layout.addStretch()
        
        # بارگذاری تنظیمات از دیتابیس
        self.load_settings()

    def load_settings(self):
        """بارگذاری تنظیمات از دیتابیس"""
        config = AppConfig.get_config()
        
        # بارگذاری تم
        theme = config.get('theme', 'روشن')
        self.theme_checkbox.setChecked(theme == 'دارک')
        
        # بارگذاری زبان
        language = config.get('language', 'فارسی')
        index = self.language_combo.findText(language)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
        
        # بارگذاری اعلان‌ها
        notifications = config.get('notifications', {})
        self.notify_checkbox.setChecked(notifications.get('enabled', True))

    def save_settings(self):
        """ذخیره تنظیمات در دیتابیس"""
        # ذخیره تم
        theme = 'دارک' if self.theme_checkbox.isChecked() else 'روشن'
        AppConfig.save_theme(theme)
        
        # ذخیره زبان
        language = self.language_combo.currentText()
        AppConfig.save_language(language)
        
        # ذخیره اعلان‌ها
        notifications_enabled = self.notify_checkbox.isChecked()
        AppConfig.save_notification_settings(notifications_enabled, notifications_enabled)

    def build_group(self, title: str, widgets: list[QWidget]) -> QFrame:
        group_box = QFrame()
        group_box.setStyleSheet("""
            QFrame {
                background-color: #2d2d30;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        group_layout = QVBoxLayout(group_box)
        group_layout.setSpacing(10)
        group_layout.addWidget(QLabel(f"<b>{title}</b>"))
        for widget in widgets:
            group_layout.addWidget(widget)
        return group_box
