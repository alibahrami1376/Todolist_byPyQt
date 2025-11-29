from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, 
    QListWidgetItem, QCheckBox, QMessageBox, QProgressBar, 
    QDateEdit, QGroupBox
)
from PyQt6.QtCore import Qt, QDate, QSize
from PyQt6.QtGui import QFont
from datetime import date
from services.habit_service import HabitService
from models.db.habit_entity import HabitEntity
from views.pages.checklist_page import HabitDialog


class HabitsPage(QWidget):
    """صفحه مدیریت عادت‌های روزانه"""
    
    def __init__(self, page_manager=None):
        super().__init__()
        self.service = HabitService()
        self.current_date = date.today()
        self.page_manager = page_manager
        self.init_ui()
        self.load_habits()
        self.apply_theme()
    
    def showEvent(self, event):
        """وقتی صفحه نمایش داده می‌شود، لیست را به‌روزرسانی کن"""
        super().showEvent(event)
        if hasattr(self, 'service'):
            self.load_habits()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # هدر با آیکون و تاریخ (مثل تصویر)
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)
        
        # ردیف اول: آیکون و "روز"
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        
        # آیکون (می‌توانید آیکون واقعی اضافه کنید)
        icon_label = QLabel("☁️☀️")
        icon_label.setFont(QFont("Segoe UI", 24))
        top_row.addWidget(icon_label)
        
        title = QLabel("روز")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        top_row.addWidget(title)
        top_row.addStretch()
        
        # دکمه‌های هفتگی و ماهانه
        btn_weekly = QPushButton("📅 هفتگی")
        btn_weekly.setFont(QFont("Segoe UI", 12))
        btn_weekly.clicked.connect(self.open_weekly)
        top_row.addWidget(btn_weekly)
        
        btn_monthly = QPushButton("📅 ماهانه")
        btn_monthly.setFont(QFont("Segoe UI", 12))
        btn_monthly.clicked.connect(self.open_monthly)
        top_row.addWidget(btn_monthly)
        
        header_layout.addLayout(top_row)
        
        # ردیف دوم: تاریخ
        date_row = QHBoxLayout()
        date_row.setContentsMargins(0, 0, 0, 0)
        
        self.date_label = QLabel()
        self.update_date_label()
        self.date_label.setFont(QFont("Segoe UI", 12))
        date_row.addWidget(self.date_label)
        date_row.addStretch()
        
        # انتخاب تاریخ
        self.date_picker = QDateEdit()
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setCalendarPopup(True)
        self.date_picker.dateChanged.connect(self.on_date_changed)
        self.date_picker.setFixedWidth(150)
        date_row.addWidget(self.date_picker)
        
        # دکمه افزودن
        add_btn = QPushButton("➕ افزودن عادت")
        add_btn.clicked.connect(self.add_habit)
        date_row.addWidget(add_btn)
        
        header_layout.addLayout(date_row)
        layout.addWidget(header_widget)
        
        # لیست عادت‌های روزانه (ساده مثل تصویر)
        self.habit_list = QListWidget()
        self.habit_list.setSpacing(5)
        layout.addWidget(self.habit_list, 1)
        
        # Progress bar در پایین (مثل تصویر)
        progress_layout = QHBoxLayout()
        self.progress_label = QLabel("0%")
        self.progress_label.setFont(QFont("Segoe UI", 12))
        progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)  # متن را در progress bar نمایش نده
        progress_layout.addWidget(self.progress_bar, 1)
        
        layout.addLayout(progress_layout)
    
    def update_date_label(self):
        """به‌روزرسانی برچسب تاریخ"""
        from datetime import datetime
        date_str = self.current_date.strftime("%B %d, %Y")
        # تبدیل به فارسی (می‌توانید کتابخانه تاریخ فارسی اضافه کنید)
        self.date_label.setText(date_str)
    
    def open_weekly(self):
        """باز کردن صفحه عادت‌های هفتگی"""
        if self.page_manager:
            try:
                self.page_manager.switch_page("habitsweekly")
            except Exception as e:
                print(f"خطا در باز کردن صفحه هفتگی: {e}")
    
    def open_monthly(self):
        """باز کردن صفحه عادت‌های ماهانه"""
        if self.page_manager:
            try:
                self.page_manager.switch_page("habitsmonthly")
            except Exception as e:
                print(f"خطا در باز کردن صفحه ماهانه: {e}")
    
    def on_date_changed(self, qdate):
        """وقتی تاریخ تغییر می‌کند"""
        self.current_date = qdate.toPyDate()
        self.update_date_label()
        self.load_habits()
    
    def load_habits(self):
        """بارگذاری عادت‌های روزانه از دیتابیس"""
        try:
            if not hasattr(self, 'habit_list'):
                return
            
            self.habit_list.clear()
            
            # دریافت فقط عادت‌های روزانه
            habits = self.service.get_habits_by_category("روزانه")
            print(f"تعداد عادت‌های روزانه بارگذاری شده: {len(habits)}")
            
            total_habits = len(habits)
            completed_habits = 0
            
            # افزودن عادت‌ها به لیست
            for habit in habits:
                try:
                    habit_id = habit.id
                    
                    item = QListWidgetItem()
                    item.setSizeHint(QSize(0, 60))
                    widget = self.create_habit_widget(habit)
                    self.habit_list.addItem(item)
                    self.habit_list.setItemWidget(item, widget)
                    
                    # بررسی تکمیل
                    if self.service.is_habit_completed_on_date(habit_id, self.current_date):
                        completed_habits += 1
                except Exception as e:
                    print(f"خطا در افزودن habit: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            # به‌روزرسانی progress bar
            if total_habits > 0:
                progress = int((completed_habits / total_habits) * 100)
                self.progress_bar.setValue(progress)
                self.progress_label.setText(f"{progress}%")
            else:
                self.progress_bar.setValue(0)
                self.progress_label.setText("0%")
                
        except Exception as e:
            print(f"خطا در بارگذاری habits: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self, "خطا", f"خطا در بارگذاری عادت‌ها: {str(e)}")
    
    def create_habit_widget(self, habit: HabitEntity):
        """ایجاد ویجت برای نمایش عادت (ساده مثل تصویر)"""
        try:
            habit_id = habit.id
            habit_title = habit.title
            
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(15, 10, 15, 10)
            layout.setSpacing(10)
            
            # چک‌باکس
            checkbox = QCheckBox(habit_title)
            checkbox.setFont(QFont("Segoe UI", 12))
            is_completed = self.service.is_habit_completed_on_date(habit_id, self.current_date)
            checkbox.setChecked(is_completed)
            checkbox.stateChanged.connect(
                lambda state, h_id=habit_id: self.toggle_habit(h_id, state == Qt.CheckState.Checked)
            )
            layout.addWidget(checkbox)
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
            
            widget.habit_id = habit_id
            widget.habit_entity = habit
            
            return widget
        except Exception as e:
            print(f"خطا در create_habit_widget: {e}")
            widget = QWidget()
            layout = QVBoxLayout(widget)
            error_label = QLabel(f"خطا در نمایش عادت: {str(e)}")
            layout.addWidget(error_label)
            return widget
    
    def toggle_habit(self, habit_id: str, checked: bool):
        """تغییر وضعیت تکمیل عادت"""
        try:
            if checked:
                self.service.log_habit(habit_id, self.current_date, value=1)
            else:
                self.service.remove_habit_log(habit_id, self.current_date)
            self.load_habits()
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در تغییر وضعیت عادت: {str(e)}")
            self.load_habits()
    
    def add_habit(self):
        """افزودن عادت جدید"""
        dialog = HabitDialog(self)
        if dialog.exec():
            habit_data = dialog.get_habit_data()
            if not habit_data["title"]:
                QMessageBox.warning(self, "خطا", "لطفاً عنوان عادت را وارد کنید.")
                return
            
            try:
                self.service.create_habit(
                    title=habit_data["title"],
                    category="روزانه",  # همیشه روزانه برای این صفحه
                    goal_type=habit_data["goal_type"],
                    daily_goal=habit_data["daily_goal"],
                    description=habit_data["description"]
                )
                self.load_habits()
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ایجاد عادت: {str(e)}")
    
    def edit_habit(self, habit: HabitEntity):
        """ویرایش عادت"""
        fresh_habit = self.service.get_habit_by_id(habit.id)
        if not fresh_habit:
            QMessageBox.warning(self, "خطا", "عادت یافت نشد.")
            self.load_habits()
            return
        
        dialog = HabitDialog(self, fresh_habit)
        if dialog.exec():
            habit_data = dialog.get_habit_data()
            if not habit_data["title"]:
                QMessageBox.warning(self, "خطا", "لطفاً عنوان عادت را وارد کنید.")
                return
            
            try:
                success = self.service.update_habit(
                    fresh_habit.id,
                    title=habit_data["title"],
                    category="روزانه",  # همیشه روزانه برای این صفحه
                    goal_type=habit_data["goal_type"],
                    daily_goal=habit_data["daily_goal"],
                    description=habit_data["description"]
                )
                if success:
                    self.load_habits()
                else:
                    QMessageBox.warning(self, "خطا", "عادت یافت نشد یا به‌روزرسانی انجام نشد.")
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ویرایش عادت: {str(e)}")
    
    def delete_habit(self, habit: HabitEntity):
        """حذف عادت"""
        reply = QMessageBox.question(
            self, "حذف عادت",
            f"آیا مطمئن هستید که می‌خواهید عادت '{habit.title}' را حذف کنید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.service.delete_habit(habit.id)
                if success:
                    self.load_habits()
                else:
                    QMessageBox.warning(self, "خطا", "عادت یافت نشد یا حذف انجام نشد.")
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در حذف عادت: {str(e)}")
    
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
                    border-radius: 4px;
                    margin: 2px;
                }
                QListWidget::item:hover {
                    background-color: #3e3e42;
                }
                QCheckBox {
                    color: white;
                }
                QGroupBox {
                    border: 2px solid #3e3e42;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QDateEdit {
                    background-color: #2d2d30;
                    color: white;
                    border: 1px solid #3e3e42;
                    border-radius: 4px;
                }
                QProgressBar {
                    border: 1px solid #3e3e42;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #0078d7;
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
                    border-radius: 4px;
                    margin: 2px;
                }
                QListWidget::item:hover {
                    background-color: #e9e9e9;
                }
                QCheckBox {
                    color: #1e1e1e;
                }
                QGroupBox {
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QDateEdit {
                    background-color: #f1f1f1;
                    color: #1e1e1e;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
                QProgressBar {
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #0078d7;
                }
            """
        
        self.setStyleSheet(style)

