from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon


class HabitLauncherPage(QWidget):
    """صفحه لانچر برای دسترسی به بخش‌های مختلف habit"""
    
    open_habits_page = pyqtSignal()
    open_reflection_page = pyqtSignal()
    open_motivation_page = pyqtSignal()
    open_statistics_page = pyqtSignal()
    
    def __init__(self, page_manager=None):
        super().__init__()
        self.page_manager = page_manager
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # عنوان
        title = QLabel("📋 مدیریت عادت‌ها")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # توضیحات
        description = QLabel("برای دسترسی به بخش مورد نظر، روی دکمه مربوطه کلیک کنید")
        description.setFont(QFont("Segoe UI", 12))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("color: gray;")
        layout.addStretch()
        layout.addWidget(description)
        
        # Grid برای دکمه‌ها
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        
        # دکمه عادت‌ها
        btn_habits = QPushButton("✅ مدیریت عادت‌ها")
        btn_habits.setMinimumHeight(120)
        btn_habits.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        btn_habits.clicked.connect(self.open_habits)
        grid_layout.addWidget(btn_habits, 0, 0)
        
        # دکمه بازتاب
        btn_reflection = QPushButton("💭 بازتاب روزانه")
        btn_reflection.setMinimumHeight(120)
        btn_reflection.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        btn_reflection.clicked.connect(self.open_reflection)
        grid_layout.addWidget(btn_reflection, 0, 1)
        
        # دکمه انگیزش
        btn_motivation = QPushButton("🌟 انگیزش روزانه")
        btn_motivation.setMinimumHeight(120)
        btn_motivation.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        btn_motivation.clicked.connect(self.open_motivation)
        grid_layout.addWidget(btn_motivation, 1, 0)
        
        # دکمه آمار
        btn_statistics = QPushButton("📊 آمار و نمودارها")
        btn_statistics.setMinimumHeight(120)
        btn_statistics.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        btn_statistics.clicked.connect(self.open_statistics)
        grid_layout.addWidget(btn_statistics, 1, 1)
        
        # استایل دکمه‌ها
        button_style = """
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
                transform: scale(1.02);
            }
            QPushButton:pressed {
                background-color: #004578;
            }
        """
        
        btn_habits.setStyleSheet(button_style)
        btn_reflection.setStyleSheet(button_style)
        btn_motivation.setStyleSheet(button_style)
        btn_statistics.setStyleSheet(button_style)
        
        # اضافه کردن grid به layout
        grid_container = QWidget()
        grid_container_layout = QVBoxLayout(grid_container)
        grid_container_layout.addLayout(grid_layout)
        grid_container_layout.setContentsMargins(100, 0, 100, 0)
        
        layout.addWidget(grid_container)
        layout.addStretch()
    
    def open_habits(self):
        """باز کردن صفحه مدیریت عادت‌ها"""
        if self.page_manager:
            from configg.page_registery import PageRegistry
            registry = PageRegistry()
            if hasattr(registry, 'habits_page'):
                self.page_manager.switch_page("habits")
        else:
            self.open_habits_page.emit()
    
    def open_reflection(self):
        """باز کردن صفحه بازتاب روزانه"""
        if self.page_manager:
            from configg.page_registery import PageRegistry
            registry = PageRegistry()
            if hasattr(registry, 'habit_reflection_page'):
                self.page_manager.switch_page("habitreflection")
        else:
            self.open_reflection_page.emit()
    
    def open_motivation(self):
        """باز کردن صفحه انگیزش روزانه"""
        if self.page_manager:
            from configg.page_registery import PageRegistry
            registry = PageRegistry()
            if hasattr(registry, 'habit_motivation_page'):
                self.page_manager.switch_page("habitmotivation")
        else:
            self.open_motivation_page.emit()
    
    def open_statistics(self):
        """باز کردن صفحه آمار و نمودارها"""
        if self.page_manager:
            from configg.page_registery import PageRegistry
            registry = PageRegistry()
            if hasattr(registry, 'habit_statistics_page'):
                self.page_manager.switch_page("habitstatistics")
        else:
            self.open_statistics_page.emit()
    
    def apply_theme(self):
        """اعمال تم"""
        from utils.app_config import AppConfig
        is_dark = AppConfig.get_theme() == "دارک"
        
        if is_dark:
            style = """
                QWidget {
                    background-color: #1e1e1e;
                    color: white;
                }
            """
        else:
            style = """
                QWidget {
                    background-color: #ffffff;
                    color: #1e1e1e;
                }
            """
        
        self.setStyleSheet(style)
