from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, 
    QListWidgetItem, QCheckBox, QMessageBox, QProgressBar, QDateEdit, QGroupBox
)
from PyQt6.QtCore import Qt, QDate, QSize
from PyQt6.QtGui import QFont
from datetime import date
from services.habit_service import HabitService
from models.db.habit_entity import HabitEntity
from views.pages.checklist_page import HabitDialog


class HabitsWeeklyPage(QWidget):
    """صفحه عادت‌های هفتگی"""
    
    def __init__(self):
        super().__init__()
        self.service = HabitService()
        self.current_date = date.today()
        self.init_ui()
        self.load_habits()
        self.apply_theme()
    
    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, 'service'):
            self.load_habits()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # هدر
        header_layout = QHBoxLayout()
        title = QLabel("📅 عادت‌های هفتگی")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # انتخاب تاریخ
        date_label = QLabel("تاریخ:")
        header_layout.addWidget(date_label)
        self.date_picker = QDateEdit()
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setCalendarPopup(True)
        self.date_picker.dateChanged.connect(self.on_date_changed)
        header_layout.addWidget(self.date_picker)
        
        # دکمه افزودن
        add_btn = QPushButton("➕ افزودن عادت")
        add_btn.clicked.connect(self.add_habit)
        header_layout.addWidget(add_btn)
        layout.addLayout(header_layout)
        
        # لیست عادت‌ها
        self.habit_list = QListWidget()
        layout.addWidget(self.habit_list, 1)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setFormat("%p% تکمیل شده")
        layout.addWidget(self.progress_bar)
    
    def on_date_changed(self, qdate):
        self.current_date = qdate.toPyDate()
        self.load_habits()
    
    def load_habits(self):
        try:
            self.habit_list.clear()
            habits = self.service.get_habits_by_category("هفتگی")
            
            total = len(habits)
            completed = 0
            
            for habit in habits:
                item = QListWidgetItem()
                item.setSizeHint(QSize(0, 60))
                widget = self.create_habit_widget(habit)
                self.habit_list.addItem(item)
                self.habit_list.setItemWidget(item, widget)
                
                if self.service.is_habit_completed_on_date(habit.id, self.current_date):
                    completed += 1
            
            if total > 0:
                progress = int((completed / total) * 100)
                self.progress_bar.setValue(progress)
            else:
                self.progress_bar.setValue(0)
        except Exception as e:
            print(f"خطا در بارگذاری عادت‌های هفتگی: {e}")
    
    def create_habit_widget(self, habit: HabitEntity):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 5, 10, 5)
        
        checkbox = QCheckBox(habit.title)
        checkbox.setFont(QFont("Segoe UI", 11))
        is_completed = self.service.is_habit_completed_on_date(habit.id, self.current_date)
        checkbox.setChecked(is_completed)
        checkbox.stateChanged.connect(
            lambda state, h_id=habit.id: self.toggle_habit(h_id, state == Qt.CheckState.Checked)
        )
        layout.addWidget(checkbox)
        layout.addStretch()
        
        edit_btn = QPushButton("✏️")
        edit_btn.setFixedSize(25, 25)
        edit_btn.clicked.connect(lambda: self.edit_habit(habit))
        layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(25, 25)
        delete_btn.clicked.connect(lambda: self.delete_habit(habit))
        layout.addWidget(delete_btn)
        
        return widget
    
    def toggle_habit(self, habit_id: str, checked: bool):
        try:
            if checked:
                self.service.log_habit(habit_id, self.current_date, value=1)
            else:
                self.service.remove_habit_log(habit_id, self.current_date)
            self.load_habits()
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در تغییر وضعیت عادت: {str(e)}")
    
    def add_habit(self):
        dialog = HabitDialog(self)
        if dialog.exec():
            habit_data = dialog.get_habit_data()
            if not habit_data["title"]:
                QMessageBox.warning(self, "خطا", "لطفاً عنوان عادت را وارد کنید.")
                return
            try:
                self.service.create_habit(
                    title=habit_data["title"],
                    category="هفتگی",
                    goal_type=habit_data["goal_type"],
                    daily_goal=habit_data["daily_goal"],
                    description=habit_data["description"]
                )
                self.load_habits()
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ایجاد عادت: {str(e)}")
    
    def edit_habit(self, habit: HabitEntity):
        fresh_habit = self.service.get_habit_by_id(habit.id)
        if not fresh_habit:
            return
        dialog = HabitDialog(self, fresh_habit)
        if dialog.exec():
            habit_data = dialog.get_habit_data()
            if not habit_data["title"]:
                return
            try:
                self.service.update_habit(
                    fresh_habit.id,
                    title=habit_data["title"],
                    category="هفتگی",
                    goal_type=habit_data["goal_type"],
                    daily_goal=habit_data["daily_goal"],
                    description=habit_data["description"]
                )
                self.load_habits()
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ویرایش عادت: {str(e)}")
    
    def delete_habit(self, habit: HabitEntity):
        reply = QMessageBox.question(
            self, "حذف عادت",
            f"آیا مطمئن هستید که می‌خواهید عادت '{habit.title}' را حذف کنید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.service.delete_habit(habit.id)
                self.load_habits()
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در حذف عادت: {str(e)}")
    
    def apply_theme(self):
        from utils.app_config import AppConfig
        is_dark = AppConfig.get_theme() == "دارک"
        
        if is_dark:
            style = """
                QWidget { background-color: #1e1e1e; color: white; }
                QPushButton { background-color: #0078d7; color: white; padding: 8px 16px; border-radius: 6px; }
                QPushButton:hover { background-color: #005a9e; }
                QListWidget { background-color: #2d2d30; border: 1px solid #3e3e42; border-radius: 8px; }
                QListWidget::item { background-color: #2d2d30; border-bottom: 1px solid #3e3e42; }
                QCheckBox { color: white; }
                QGroupBox { border: 2px solid #3e3e42; border-radius: 8px; margin-top: 10px; padding-top: 10px; }
                QDateEdit { background-color: #2d2d30; color: white; border: 1px solid #3e3e42; border-radius: 4px; }
                QProgressBar { border: 1px solid #3e3e42; border-radius: 4px; text-align: center; }
                QProgressBar::chunk { background-color: #0078d7; }
            """
        else:
            style = """
                QWidget { background-color: #ffffff; color: #1e1e1e; }
                QPushButton { background-color: #0078d7; color: white; padding: 8px 16px; border-radius: 6px; }
                QPushButton:hover { background-color: #005a9e; }
                QListWidget { background-color: #f1f1f1; border: 1px solid #ddd; border-radius: 8px; }
                QListWidget::item { background-color: #ffffff; border-bottom: 1px solid #ddd; }
                QCheckBox { color: #1e1e1e; }
                QGroupBox { border: 2px solid #ddd; border-radius: 8px; margin-top: 10px; padding-top: 10px; }
                QDateEdit { background-color: #f1f1f1; color: #1e1e1e; border: 1px solid #ddd; border-radius: 4px; }
                QProgressBar { border: 1px solid #ddd; border-radius: 4px; text-align: center; }
                QProgressBar::chunk { background-color: #0078d7; }
            """
        self.setStyleSheet(style)

