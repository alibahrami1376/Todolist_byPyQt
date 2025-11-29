from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QDateEdit
)
from PyQt6.QtCore import Qt, QDate, QRect
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QBrush
from datetime import date, timedelta
from services.habit_service import HabitService
from views.pages.checklist_page import ProgressChartWidget


class HabitStatisticsPage(QWidget):
    """صفحه آمار و نمودارهای عادت‌ها"""
    
    def __init__(self):
        super().__init__()
        self.service = HabitService()
        self.current_date = date.today()
        self.init_ui()
        self.update_visualizations()
        self.apply_theme()
    
    def showEvent(self, event):
        """وقتی صفحه نمایش داده می‌شود"""
        super().showEvent(event)
        if hasattr(self, 'service'):
            self.update_visualizations()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # هدر
        header_layout = QHBoxLayout()
        title = QLabel("📊 آمار و نمودارها")
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
        
        layout.addLayout(header_layout)
        
        # Tab برای نمودارها
        charts_tabs = QTabWidget()
        
        # نمودار روزانه
        daily_chart_widget = QWidget()
        daily_layout = QVBoxLayout(daily_chart_widget)
        daily_layout.setContentsMargins(10, 10, 10, 10)
        daily_layout.setSpacing(10)
        daily_label = QLabel("پیشرفت 7 روز گذشته:")
        daily_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        daily_layout.addWidget(daily_label)
        self.daily_chart = ProgressChartWidget()
        self.daily_chart.setMinimumHeight(300)
        daily_layout.addWidget(self.daily_chart)
        daily_layout.addStretch()
        charts_tabs.addTab(daily_chart_widget, "روزانه")
        
        # نمودار هفتگی
        weekly_chart_widget = QWidget()
        weekly_layout = QVBoxLayout(weekly_chart_widget)
        weekly_layout.setContentsMargins(10, 10, 10, 10)
        weekly_layout.setSpacing(10)
        weekly_label = QLabel("پیشرفت 4 هفته گذشته:")
        weekly_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        weekly_layout.addWidget(weekly_label)
        self.weekly_chart = ProgressChartWidget()
        self.weekly_chart.setMinimumHeight(300)
        weekly_layout.addWidget(self.weekly_chart)
        weekly_layout.addStretch()
        charts_tabs.addTab(weekly_chart_widget, "هفتگی")
        
        # نمودار ماهانه
        monthly_chart_widget = QWidget()
        monthly_layout = QVBoxLayout(monthly_chart_widget)
        monthly_layout.setContentsMargins(10, 10, 10, 10)
        monthly_layout.setSpacing(10)
        monthly_label = QLabel("پیشرفت 6 ماه گذشته:")
        monthly_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        monthly_layout.addWidget(monthly_label)
        self.monthly_chart = ProgressChartWidget()
        self.monthly_chart.setMinimumHeight(300)
        monthly_layout.addWidget(self.monthly_chart)
        monthly_layout.addStretch()
        charts_tabs.addTab(monthly_chart_widget, "ماهانه")
        
        layout.addWidget(charts_tabs)
        
        # آمار کلی
        from PyQt6.QtWidgets import QGroupBox
        stats_group = QGroupBox("📊 آمار کلی")
        stats_layout = QVBoxLayout()
        
        self.stats_label = QLabel()
        self.stats_label.setWordWrap(True)
        self.stats_label.setFont(QFont("Segoe UI", 11))
        stats_layout.addWidget(self.stats_label)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        layout.addStretch()
    
    def on_date_changed(self, qdate):
        """وقتی تاریخ تغییر می‌کند"""
        self.current_date = qdate.toPyDate()
        self.update_visualizations()
    
    def update_visualizations(self):
        """به‌روزرسانی نمودارها و آمار"""
        try:
            habits = self.service.get_all_habits(active_only=True)
            
            # نمودار روزانه (7 روز گذشته)
            daily_data = []
            for i in range(6, -1, -1):
                check_date = self.current_date - timedelta(days=i)
                completed = sum(1 for h in habits 
                              if self.service.is_habit_completed_on_date(h.id, check_date))
                total = len(habits)
                percentage = (completed / total * 100) if total > 0 else 0
                daily_data.append((check_date, percentage))
            self.daily_chart.set_data(daily_data)
            
            # نمودار هفتگی (4 هفته گذشته)
            weekly_data = []
            for i in range(3, -1, -1):
                week_start = self.current_date - timedelta(weeks=i, days=self.current_date.weekday())
                week_end = week_start + timedelta(days=6)
                completed_days = sum(1 for day_offset in range(7)
                                   if any(self.service.is_habit_completed_on_date(h.id, week_start + timedelta(days=day_offset))
                                         for h in habits))
                percentage = (completed_days / (len(habits) * 7) * 100) if habits else 0
                weekly_data.append((week_start, percentage))
            self.weekly_chart.set_data(weekly_data)
            
            # نمودار ماهانه (6 ماه گذشته)
            monthly_data = []
            for i in range(5, -1, -1):
                month_date = date(self.current_date.year, self.current_date.month, 1)
                if month_date.month - i <= 0:
                    month_date = date(month_date.year - 1, 12 + (month_date.month - i), 1)
                else:
                    month_date = date(month_date.year, month_date.month - i, 1)
                
                # محاسبه آمار ماه
                stats = self.service.get_habit_statistics(
                    habits[0].id if habits else "", 
                    month_date, 
                    date(month_date.year, month_date.month, 28)
                ) if habits else {}
                percentage = stats.get('success_rate', 0)
                monthly_data.append((month_date, percentage))
            self.monthly_chart.set_data(monthly_data)
            
            # آمار کلی
            total_habits = len(habits)
            today_completed = sum(1 for h in habits 
                                if self.service.is_habit_completed_on_date(h.id, self.current_date))
            week_completed = sum(1 for h in habits
                               for day_offset in range(7)
                               if self.service.is_habit_completed_on_date(h.id, self.current_date - timedelta(days=day_offset)))
            
            stats_text = f"""
            <b>آمار امروز:</b><br>
            ✅ تکمیل شده: {today_completed}/{total_habits}<br>
            <b>آمار هفته:</b><br>
            ✅ تکمیل شده: {week_completed} عادت-روز<br>
            <b>نرخ موفقیت:</b><br>
            📈 {((today_completed / total_habits * 100) if total_habits > 0 else 0):.1f}%
            """
            self.stats_label.setText(stats_text)
            
        except Exception as e:
            print(f"خطا در به‌روزرسانی نمودارها: {e}")
            import traceback
            traceback.print_exc()
    
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
            """
        else:
            style = """
                QWidget {
                    background-color: #ffffff;
                    color: #1e1e1e;
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
            """
        
        self.setStyleSheet(style)

