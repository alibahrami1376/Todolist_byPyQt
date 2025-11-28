from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QListWidget, QListWidgetItem, QCheckBox, QDialog, QComboBox, QTextEdit,
    QTabWidget, QMessageBox, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate, QSize
from PyQt6.QtGui import QFont, QIcon
import os
from datetime import datetime, date
from services.habit_service import HabitService
from models.db.habit_entity import HabitEntity


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
        config_path = "configg/theme_config.txt"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    theme = f.read().strip() or "روشن"
                    return theme == "دارک"
            except Exception:
                return True
        return True


class ChecklistPage(QWidget):
    """صفحه چک‌لیست عادت‌ها"""
    
    def __init__(self):
        super().__init__()
        self.service = HabitService()
        self.current_date = date.today()
        self.init_ui()
        self.load_habits()
        self.apply_theme()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # هدر
        header_layout = QHBoxLayout()
        title = QLabel("📋 چک‌لیست عادت‌ها")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # دکمه افزودن
        add_btn = QPushButton("➕ افزودن عادت")
        add_btn.clicked.connect(self.add_habit)
        header_layout.addWidget(add_btn)
        layout.addLayout(header_layout)
        
        # Tab برای انواع عادت‌ها
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_habit_list("روزانه"), "روزانه")
        self.tabs.addTab(self.create_habit_list("هفتگی"), "هفتگی")
        self.tabs.addTab(self.create_habit_list("ماهانه"), "ماهانه")
        self.tabs.addTab(self.create_habit_list("سالانه"), "سالانه")
        layout.addWidget(self.tabs)
    
    def create_habit_list(self, category: str):
        """ایجاد لیست عادت‌ها برای یک دسته خاص"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        list_widget = QListWidget()
        list_widget.setObjectName(f"habit_list_{category}")
        layout.addWidget(list_widget)
        
        return widget
    
    def load_habits(self):
        """بارگذاری عادت‌ها از دیتابیس"""
        habits = self.service.get_all_habits(active_only=True)
        
        # پاک کردن لیست‌ها
        for i in range(self.tabs.count()):
            tab_widget = self.tabs.widget(i)
            list_widget = tab_widget.findChild(QListWidget)
            if list_widget:
                list_widget.clear()
        
        # افزودن عادت‌ها به لیست مربوطه
        for habit in habits:
            category = habit.category or "روزانه"
            tab_index = ["روزانه", "هفتگی", "ماهانه", "سالانه"].index(category)
            tab_widget = self.tabs.widget(tab_index)
            list_widget = tab_widget.findChild(QListWidget)
            
            if list_widget:
                item = self.create_habit_item(habit)
                list_widget.addItem(item)
                list_widget.setItemWidget(item, self.create_habit_widget(habit))
    
    def create_habit_item(self, habit: HabitEntity):
        """ایجاد آیتم لیست برای عادت"""
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, habit.id)
        item.setSizeHint(QSize(0, 70))
        return item
    
    def create_habit_widget(self, habit: HabitEntity):
        """ایجاد ویجت برای نمایش عادت"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # چک‌باکس
        checkbox = QCheckBox()
        is_completed = self.service.is_habit_completed_on_date(habit.id, self.current_date)
        checkbox.setChecked(is_completed)
        checkbox.stateChanged.connect(
            lambda state, h_id=habit.id: self.toggle_habit(h_id, state == Qt.CheckState.Checked)
        )
        layout.addWidget(checkbox)
        
        # اطلاعات عادت
        text_layout = QVBoxLayout()
        name_label = QLabel(habit.title)
        name_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        text_layout.addWidget(name_label)
        
        # نمایش نوع هدف و مقدار
        goal_info = f"هدف: {habit.daily_goal}"
        if habit.goal_type == "count":
            goal_info += " عدد"
        elif habit.goal_type == "time":
            goal_info += " دقیقه"
        
        goal_label = QLabel(goal_info)
        goal_label.setStyleSheet("color: gray; font-size: 10px;")
        text_layout.addWidget(goal_label)
        
        if habit.description:
            desc_label = QLabel(habit.description)
            desc_label.setStyleSheet("color: gray; font-size: 10px;")
            desc_label.setWordWrap(True)
            text_layout.addWidget(desc_label)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        # دکمه‌های ویرایش و حذف
        edit_btn = QPushButton("✏️")
        edit_btn.setFixedSize(30, 30)
        edit_btn.clicked.connect(lambda: self.edit_habit(habit))
        layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(30, 30)
        delete_btn.clicked.connect(lambda: self.delete_habit(habit))
        layout.addWidget(delete_btn)
        
        return widget
    
    def toggle_habit(self, habit_id: str, checked: bool):
        """تغییر وضعیت تکمیل عادت"""
        if checked:
            self.service.log_habit(habit_id, self.current_date, value=1)
        else:
            self.service.remove_habit_log(habit_id, self.current_date)
        self.load_habits()  # بارگذاری مجدد
    
    def add_habit(self):
        """افزودن عادت جدید"""
        dialog = HabitDialog(self)
        if dialog.exec():
            habit_data = dialog.get_habit_data()
            if not habit_data["title"]:
                QMessageBox.warning(self, "خطا", "لطفاً عنوان عادت را وارد کنید.")
                return
            
            self.service.create_habit(
                title=habit_data["title"],
                category=habit_data["category"],
                goal_type=habit_data["goal_type"],
                daily_goal=habit_data["daily_goal"],
                description=habit_data["description"]
            )
            self.load_habits()
    
    def edit_habit(self, habit: HabitEntity):
        """ویرایش عادت"""
        dialog = HabitDialog(self, habit)
        if dialog.exec():
            habit_data = dialog.get_habit_data()
            if not habit_data["title"]:
                QMessageBox.warning(self, "خطا", "لطفاً عنوان عادت را وارد کنید.")
                return
            
            self.service.update_habit(
                habit.id,
                title=habit_data["title"],
                category=habit_data["category"],
                goal_type=habit_data["goal_type"],
                daily_goal=habit_data["daily_goal"],
                description=habit_data["description"]
            )
            self.load_habits()
    
    def delete_habit(self, habit: HabitEntity):
        """حذف عادت"""
        reply = QMessageBox.question(
            self, "حذف عادت",
            f"آیا مطمئن هستید که می‌خواهید عادت '{habit.title}' را حذف کنید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.service.delete_habit(habit.id)
            self.load_habits()
    
    def apply_theme(self):
        """اعمال تم"""
        is_dark = self.get_current_theme()
        
        if is_dark:
            style = """
                QWidget {
                    background-color: #1e1e1e;
                    color: white;
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
                QListWidget {
                    background-color: #2d2d30;
                    border: 1px solid #3e3e42;
                    border-radius: 8px;
                }
                QListWidget::item {
                    background-color: #2d2d30;
                    border-bottom: 1px solid #3e3e42;
                }
                QListWidget::item:hover {
                    background-color: #3e3e42;
                }
                QTabWidget::pane {
                    border: 1px solid #3e3e42;
                    background-color: #1e1e1e;
                }
                QTabBar::tab {
                    background-color: #2d2d30;
                    color: white;
                    padding: 8px 16px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background-color: #0078d7;
                }
                QCheckBox {
                    color: white;
                }
            """
        else:
            style = """
                QWidget {
                    background-color: #ffffff;
                    color: #1e1e1e;
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
                QListWidget {
                    background-color: #f1f1f1;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                }
                QListWidget::item {
                    background-color: #ffffff;
                    border-bottom: 1px solid #ddd;
                }
                QListWidget::item:hover {
                    background-color: #e9e9e9;
                }
                QTabWidget::pane {
                    border: 1px solid #ddd;
                    background-color: #ffffff;
                }
                QTabBar::tab {
                    background-color: #f1f1f1;
                    color: #1e1e1e;
                    padding: 8px 16px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background-color: #0078d7;
                    color: white;
                }
                QCheckBox {
                    color: #1e1e1e;
                }
            """
        
        self.setStyleSheet(style)
    
    def get_current_theme(self):
        """دریافت تم فعلی"""
        config_path = "configg/theme_config.txt"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    theme = f.read().strip() or "روشن"
                    return theme == "دارک"
            except Exception:
                return True
        return True
