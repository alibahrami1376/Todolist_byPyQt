"""
صفحه تنظیمات اولیه برای اولین اجرای برنامه
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QDateTimeEdit, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, QDateTime, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from datetime import datetime
from utils.time_fetcher import TimeFetcher
from utils.app_config import AppConfig

class FirstRunSettingsDialog(QDialog):
    """دیالوگ تنظیمات اولیه"""
    
    setup_completed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("تنظیمات اولیه برنامه")
        self.setMinimumSize(500, 400)
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowTitleHint | 
                           Qt.WindowType.WindowCloseButtonHint)
        
        # اعمال استایل دارک به دیالوگ
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: white;
            }
            QLabel {
                color: white;
            }
        """)
        
        self.init_ui()
        self.fetch_time_from_internet()
    
    def init_ui(self):
        """ایجاد رابط کاربری"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # عنوان
        title = QLabel("خوش آمدید! تنظیمات اولیه")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # توضیحات
        desc = QLabel("لطفاً تاریخ و زمان سیستم خود را تنظیم کنید.\n"
                     "در حال دریافت زمان از اینترنت...")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)
        self.desc_label = desc
        
        # فریم برای تاریخ و زمان
        datetime_frame = QFrame()
        datetime_frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d30;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        datetime_layout = QVBoxLayout(datetime_frame)
        datetime_layout.setSpacing(15)
        
        # برچسب تاریخ
        date_label = QLabel("تاریخ:")
        date_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        datetime_layout.addWidget(date_label)
        
        # ویرایشگر تاریخ
        self.date_edit = QDateTimeEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy/MM/dd")
        self.date_edit.setDate(datetime.now().date())
        self.date_edit.setStyleSheet("""
            QDateTimeEdit {
                background-color: #1e1e1e;
                border: 2px solid #3e3e42;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
            QDateTimeEdit:hover {
                border-color: #0078d7;
            }
            QDateTimeEdit:focus {
                border-color: #0078d7;
            }
        """)
        datetime_layout.addWidget(self.date_edit)
        
        # برچسب زمان
        time_label = QLabel("زمان:")
        time_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        datetime_layout.addWidget(time_label)
        
        # ویرایشگر زمان
        self.time_edit = QDateTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setTime(datetime.now().time())
        self.time_edit.setStyleSheet("""
            QDateTimeEdit {
                background-color: #1e1e1e;
                border: 2px solid #3e3e42;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
            QDateTimeEdit:hover {
                border-color: #0078d7;
            }
            QDateTimeEdit:focus {
                border-color: #0078d7;
            }
        """)
        datetime_layout.addWidget(self.time_edit)
        
        layout.addWidget(datetime_frame)
        
        # دکمه‌ها
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # دکمه دریافت مجدد از اینترنت
        self.refresh_btn = QPushButton("🔄 دریافت مجدد از اینترنت")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005fa1;
            }
            QPushButton:pressed {
                background-color: #004578;
            }
        """)
        self.refresh_btn.clicked.connect(self.fetch_time_from_internet)
        buttons_layout.addWidget(self.refresh_btn)
        
        # دکمه تایید
        self.confirm_btn = QPushButton("✓ تایید و ادامه")
        self.confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 30px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0e6b0e;
            }
            QPushButton:pressed {
                background-color: #0c5a0c;
            }
        """)
        self.confirm_btn.clicked.connect(self.confirm_settings)
        buttons_layout.addWidget(self.confirm_btn)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
    
    def fetch_time_from_internet(self):
        """دریافت زمان از اینترنت"""
        self.desc_label.setText("در حال دریافت زمان از اینترنت...")
        self.refresh_btn.setEnabled(False)
        self.confirm_btn.setEnabled(False)
        
        # استفاده از QTimer برای انجام کار در پس‌زمینه (غیرمسدودکننده)
        QTimer.singleShot(100, self._do_fetch_time)
    
    def _do_fetch_time(self):
        """انجام دریافت زمان"""
        result = TimeFetcher.fetch_time_from_internet()
        
        if result:
            dt, timezone = result
            # تنظیم تاریخ و زمان
            qdt = QDateTime.fromSecsSinceEpoch(int(dt.timestamp()))
            self.date_edit.setDateTime(qdt)
            self.time_edit.setDateTime(qdt)
            
            self.desc_label.setText(
                f"زمان از اینترنت دریافت شد.\n"
                f"منطقه زمانی: {timezone}\n"
                f"اگر درست است تایید کنید، در غیر این صورت ویرایش کنید."
            )
        else:
            # در صورت خطا، استفاده از زمان محلی
            local_dt = TimeFetcher.get_local_time()
            qdt = QDateTime.fromSecsSinceEpoch(int(local_dt.timestamp()))
            self.date_edit.setDateTime(qdt)
            self.time_edit.setDateTime(qdt)
            
            self.desc_label.setText(
                "خطا در دریافت زمان از اینترنت.\n"
                "زمان محلی سیستم نمایش داده شد.\n"
                "لطفاً تاریخ و زمان را بررسی و در صورت نیاز ویرایش کنید."
            )
            
            QMessageBox.warning(
                self,
                "خطا در دریافت زمان",
                "نمی‌توان به اینترنت متصل شد.\n"
                "زمان محلی سیستم استفاده می‌شود.\n"
                "لطفاً تاریخ و زمان را بررسی کنید."
            )
        
        self.refresh_btn.setEnabled(True)
        self.confirm_btn.setEnabled(True)
    
    def confirm_settings(self):
        """تایید تنظیمات"""
        # ترکیب تاریخ و زمان
        date = self.date_edit.date()
        time = self.time_edit.time()
        combined_dt = QDateTime(date, time)
        dt = combined_dt.toPyDateTime()
        
        # فرمت کردن
        date_str, time_str = TimeFetcher.format_datetime(dt)
        
        # ذخیره تنظیمات
        AppConfig.save_datetime_settings(date_str, time_str)
        AppConfig.mark_setup_complete()
        
        # نمایش پیام موفقیت
        QMessageBox.information(
            self,
            "تنظیمات ذخیره شد",
            "تنظیمات با موفقیت ذخیره شد.\n"
            "برنامه آماده استفاده است."
        )
        
        # ارسال سیگنال
        self.setup_completed.emit()
        
        # بستن دیالوگ
        self.accept()
    
    def closeEvent(self, event):
        """مدیریت بستن دیالوگ"""
        # اگر تنظیمات کامل نشده، از کاربر تایید بگیر
        if not AppConfig.is_setup_complete():
            reply = QMessageBox.question(
                self,
                "تایید خروج",
                "آیا مطمئن هستید که می‌خواهید بدون تنظیم تاریخ و زمان خارج شوید؟\n"
                "برنامه بدون تنظیمات اولیه کار نمی‌کند.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
        
        event.accept()

