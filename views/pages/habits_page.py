from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, 
    QListWidgetItem, QCheckBox, QMessageBox, QTabWidget, QProgressBar, 
    QDateEdit, QGroupBox
)
from PyQt6.QtCore import Qt, QDate, QSize
from PyQt6.QtGui import QFont
from datetime import date
from services.habit_service import HabitService
from models.db.habit_entity import HabitEntity
from views.pages.checklist_page import HabitDialog


class HabitsPage(QWidget):
    """صفحه مدیریت عادت‌ها"""
    
    def __init__(self):
        super().__init__()
        self.service = HabitService()
        self.current_date = date.today()
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
        
        # هدر
        header_layout = QHBoxLayout()
        title = QLabel("✅ مدیریت عادت‌ها")
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
        
        # بخش عادت‌ها
        habits_group = QGroupBox("✅ عادت‌های روزانه")
        habits_layout = QVBoxLayout()
        
        # Progress bar کلی
        self.overall_progress = QProgressBar()
        self.overall_progress.setMinimum(0)
        self.overall_progress.setMaximum(100)
        self.overall_progress.setFormat("%p% تکمیل شده")
        habits_layout.addWidget(self.overall_progress)
        
        # Tab برای انواع عادت‌ها
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_habit_list("روزانه"), "روزانه")
        self.tabs.addTab(self.create_habit_list("هفتگی"), "هفتگی")
        self.tabs.addTab(self.create_habit_list("ماهانه"), "ماهانه")
        self.tabs.addTab(self.create_habit_list("سالانه"), "سالانه")
        habits_layout.addWidget(self.tabs)
        habits_group.setLayout(habits_layout)
        layout.addWidget(habits_group)
    
    def on_date_changed(self, qdate):
        """وقتی تاریخ تغییر می‌کند"""
        self.current_date = qdate.toPyDate()
        self.load_habits()
    
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
        try:
            # پاک کردن لیست‌ها اول
            for i in range(self.tabs.count()):
                tab_widget = self.tabs.widget(i)
                list_widget = tab_widget.findChild(QListWidget)
                if list_widget:
                    list_widget.clear()
            
            # دریافت عادت‌ها از دیتابیس
            habits = self.service.get_all_habits(active_only=True)
            
            total_habits = len(habits)
            completed_habits = 0
            
            # افزودن عادت‌ها به لیست مربوطه
            for habit in habits:
                try:
                    habit_id = habit.id
                    habit_category = habit.category or "روزانه"
                    
                    if habit_category not in ["روزانه", "هفتگی", "ماهانه", "سالانه"]:
                        habit_category = "روزانه"
                    
                    tab_index = ["روزانه", "هفتگی", "ماهانه", "سالانه"].index(habit_category)
                    tab_widget = self.tabs.widget(tab_index)
                    list_widget = tab_widget.findChild(QListWidget)
                    
                    if list_widget:
                        item = self.create_habit_item(habit)
                        list_widget.addItem(item)
                        widget = self.create_habit_widget(habit)
                        list_widget.setItemWidget(item, widget)
                        
                        # بررسی تکمیل
                        if self.service.is_habit_completed_on_date(habit_id, self.current_date):
                            completed_habits += 1
                except Exception as e:
                    print(f"خطا در افزودن habit: {e}")
                    continue
            
            # به‌روزرسانی progress bar
            if total_habits > 0:
                progress = int((completed_habits / total_habits) * 100)
                self.overall_progress.setValue(progress)
            else:
                self.overall_progress.setValue(0)
                
        except Exception as e:
            print(f"خطا در بارگذاری habits: {e}")
            import traceback
            traceback.print_exc()
    
    def create_habit_item(self, habit: HabitEntity):
        """ایجاد آیتم لیست برای عادت"""
        try:
            habit_id = habit.id
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, habit_id)
            item.setSizeHint(QSize(0, 80))
            return item
        except Exception as e:
            print(f"خطا در create_habit_item: {e}")
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 80))
            return item
    
    def create_habit_widget(self, habit: HabitEntity):
        """ایجاد ویجت برای نمایش عادت با progress bar"""
        try:
            habit_id = habit.id
            habit_title = habit.title
            habit_goal_type = habit.goal_type or "boolean"
            habit_daily_goal = habit.daily_goal or 1
            habit_description = habit.description or ""
            
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(10, 5, 10, 5)
            layout.setSpacing(5)
            
            # ردیف اول: چک‌باکس و عنوان
            top_layout = QHBoxLayout()
            
            checkbox = QCheckBox(habit_title)
            checkbox.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            is_completed = self.service.is_habit_completed_on_date(habit_id, self.current_date)
            checkbox.setChecked(is_completed)
            checkbox.stateChanged.connect(
                lambda state, h_id=habit_id: self.toggle_habit(h_id, state == Qt.CheckState.Checked)
            )
            top_layout.addWidget(checkbox)
            top_layout.addStretch()
            
            # دکمه‌های ویرایش و حذف
            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(25, 25)
            edit_btn.clicked.connect(lambda: self.edit_habit(habit))
            top_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setFixedSize(25, 25)
            delete_btn.clicked.connect(lambda: self.delete_habit(habit))
            top_layout.addWidget(delete_btn)
            
            layout.addLayout(top_layout)
            
            # Progress bar برای عادت‌های count/time
            if habit_goal_type in ["count", "time"]:
                # دریافت مقدار فعلی از لاگ‌ها
                logs = self.service.get_habit_logs(habit_id, self.current_date, self.current_date)
                current_value = logs[0].value if logs else 0
                
                progress_bar = QProgressBar()
                progress_bar.setMinimum(0)
                progress_bar.setMaximum(habit_daily_goal)
                progress_bar.setValue(current_value)
                progress_bar.setFormat(f"{current_value}/{habit_daily_goal}")
                layout.addWidget(progress_bar)
            
            # توضیحات
            if habit_description:
                desc_label = QLabel(habit_description)
                desc_label.setStyleSheet("color: gray; font-size: 9px;")
                desc_label.setWordWrap(True)
                layout.addWidget(desc_label)
            
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
                    category=habit_data["category"],
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
                    category=habit_data["category"],
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

