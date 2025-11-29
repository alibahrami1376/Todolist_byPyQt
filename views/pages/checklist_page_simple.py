# این فایل جایگزین فایل checklist_page.py اصلی می‌شود
# برای استفاده: محتوای این فایل را در checklist_page.py کپی کنید

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QListWidget, QListWidgetItem, QCheckBox, QDialog, QComboBox, QTextEdit,
    QTabWidget, QMessageBox, QSpinBox, QFrame, QProgressBar, QScrollArea,
    QDateEdit, QGroupBox, QSplitter, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate, QSize, QRect
from PyQt6.QtGui import QFont, QIcon, QPainter, QColor, QPen, QBrush
import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from services.habit_service import HabitService
from models.db.habit_entity import HabitEntity
from services.db_session import get_session
from models.db.habit_entity import HabitLogEntity
from sqlalchemy import select, func, and_


class HabitDialog(QDialog):
    """دیالوگ برای افزودن/ویرایش عادت"""
    
    def __init__(self, parent=None, habit: HabitEntity = None):
        super().__init__(parent)
        self.habit = habit
        self.setWindowTitle("افزودن عادت جدید" if not habit else "ویرایش عادت")
        self.setMinimumWidth(450)
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # عنوان عادت
        title_label = QLabel("عنوان عادت:")
        layout.addWidget(title_label)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("مثلاً: ورزش، مطالعه، نوشیدن آب...")
        if self.habit:
            self.title_input.setText(self.habit.title)
        layout.addWidget(self.title_input)
        
        # دسته‌بندی (نوع عادت)
        category_label = QLabel("نوع عادت:")
        layout.addWidget(category_label)
        self.category_combo = QComboBox()
        self.category_combo.addItems(["روزانه", "هفتگی", "ماهانه", "سالانه"])
        if self.habit:
            category_index = ["روزانه", "هفتگی", "ماهانه", "سالانه"].index(
                self.habit.category if self.habit.category else "روزانه"
            )
            self.category_combo.setCurrentIndex(category_index)
        layout.addWidget(self.category_combo)
        
        # نوع هدف
        goal_type_label = QLabel("نوع هدف:")
        layout.addWidget(goal_type_label)
        self.goal_type_combo = QComboBox()
        self.goal_type_combo.addItems(["boolean", "count", "time"])
        self.goal_type_combo.setToolTip("boolean: انجام/عدم انجام\ncount: تعداد (مثلاً 10 صفحه)\ntime: زمان (مثلاً 30 دقیقه)")
        if self.habit:
            goal_index = ["boolean", "count", "time"].index(
                self.habit.goal_type if self.habit.goal_type else "boolean"
            )
            self.goal_type_combo.setCurrentIndex(goal_index)
        layout.addWidget(self.goal_type_combo)
        
        # هدف روزانه
        daily_goal_label = QLabel("هدف روزانه:")
        layout.addWidget(daily_goal_label)
        self.daily_goal_spin = QSpinBox()
        self.daily_goal_spin.setMinimum(1)
        self.daily_goal_spin.setMaximum(1000)
        if self.habit:
            self.daily_goal_spin.setValue(self.habit.daily_goal or 1)
        else:
            self.daily_goal_spin.setValue(1)
        layout.addWidget(self.daily_goal_spin)
        
        # توضیحات
        desc_label = QLabel("توضیحات (اختیاری):")
        layout.addWidget(desc_label)
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        if self.habit:
            self.desc_input.setPlainText(self.habit.description or "")
        layout.addWidget(self.desc_input)
        
        # دکمه‌ها
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("ذخیره")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("لغو")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
    
    def get_habit_data(self):
        """دریافت داده‌های عادت"""
        return {
            "title": self.title_input.text().strip(),
            "category": self.category_combo.currentText(),
            "goal_type": self.goal_type_combo.currentText(),
            "daily_goal": self.daily_goal_spin.value(),
            "description": self.desc_input.toPlainText().strip() or None
        }
    
    def apply_theme(self):
        is_dark = self.get_current_theme()
        if is_dark:
            style = """
                QWidget {
                    background-color: #1e1e1e;
                    color: white;
                }
                QLineEdit, QTextEdit, QComboBox, QSpinBox {
                    background-color: #2d2d30;
                    color: white;
                    border: 1px solid #3e3e42;
                    border-radius: 4px;
                    padding: 6px;
                }
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
            """
        else:
            style = """
                QWidget {
                    background-color: #ffffff;
                    color: #1e1e1e;
                }
                QLineEdit, QTextEdit, QComboBox, QSpinBox {
                    background-color: #f1f1f1;
                    color: #1e1e1e;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 6px;
                }
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
            """
        self.setStyleSheet(style)
    
    def get_current_theme(self):
        from utils.app_config import AppConfig
        return AppConfig.get_theme() == "دارک"


class ProgressChartWidget(QWidget):
    """ویجت برای نمایش نمودار پیشرفت"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []  # لیست tuples: (date, value)
        self.setMinimumHeight(200)
        self.setMinimumWidth(400)
    
    def set_data(self, data: List[tuple]):
        """تنظیم داده‌های نمودار"""
        self.data = data
        self.update()
    
    def paintEvent(self, event):
        """رسم نمودار"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        margin = 40
        chart_rect = QRect(margin, margin, rect.width() - 2 * margin, rect.height() - 2 * margin)
        
        if not self.data or len(self.data) == 0:
            painter.setPen(QColor(128, 128, 128))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "داده‌ای برای نمایش وجود ندارد")
            return
        
        # محاسبه مقادیر min و max
        values = [v for _, v in self.data]
        if not values:
            return
        
        min_val = min(values)
        max_val = max(values)
        if max_val == min_val:
            max_val = min_val + 1
        
        # رسم محورها
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        painter.drawLine(chart_rect.left(), chart_rect.bottom(), chart_rect.right(), chart_rect.bottom())
        painter.drawLine(chart_rect.left(), chart_rect.top(), chart_rect.left(), chart_rect.bottom())
        
        # رسم خط نمودار
        if len(self.data) > 1:
            painter.setPen(QPen(QColor(0, 120, 215), 2))
            points = []
            for i, (d, v) in enumerate(self.data):
                x = chart_rect.left() + (i / (len(self.data) - 1)) * chart_rect.width()
                y = chart_rect.bottom() - ((v - min_val) / (max_val - min_val)) * chart_rect.height()
                points.append((x, y))
            
            for i in range(len(points) - 1):
                painter.drawLine(int(points[i][0]), int(points[i][1]), 
                               int(points[i+1][0]), int(points[i+1][1]))
        
        # رسم نقاط
        painter.setBrush(QBrush(QColor(0, 120, 215)))
        for i, (d, v) in enumerate(self.data):
            x = chart_rect.left() + (i / max(1, len(self.data) - 1)) * chart_rect.width()
            y = chart_rect.bottom() - ((v - min_val) / (max_val - min_val)) * chart_rect.height()
            painter.drawEllipse(int(x) - 3, int(y) - 3, 6, 6)


class ChecklistPage(QWidget):
    """صفحه لانچر Habit Tracker - تقسیم شده برای عملکرد بهتر"""
    
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
            self.page_manager.switch_page("habits")
    
    def open_reflection(self):
        """باز کردن صفحه بازتاب روزانه"""
        if self.page_manager:
            self.page_manager.switch_page("habitreflection")
    
    def open_motivation(self):
        """باز کردن صفحه انگیزش روزانه"""
        if self.page_manager:
            self.page_manager.switch_page("habitmotivation")
    
    def open_statistics(self):
        """باز کردن صفحه آمار و نمودارها"""
        if self.page_manager:
            self.page_manager.switch_page("habitstatistics")
    
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

