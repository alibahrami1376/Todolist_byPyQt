from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
import os


class MoreFeaturesPage(QWidget):
    # Signal برای تغییر صفحه
    feature_clicked = pyqtSignal(str)
    
    def __init__(self, page_manager=None):
        super().__init__()
        self.page_manager = page_manager
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # عنوان صفحه
        title = QLabel("امکانات بیشتر")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # توضیحات
        description = QLabel("انتخاب کنید کدام امکان را می‌خواهید استفاده کنید:")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)
        
        # Grid layout برای کارت‌های امکانات
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setContentsMargins(20, 20, 20, 20)
        
        # لیست امکانات
        features = [
            {
                "name": "تقویم",
                "icon": "calendar.png",
                "description": "تقویم و مدیریت رویدادها",
                "page": "Calendar"
            },
            {
                "name": "یادداشت روزانه",
                "icon": "journal.png",
                "description": "یادداشت‌های روزانه و خاطرات",
                "page": "Journal"
            },
            {
                "name": "لیست کارها",
                "icon": "todolist.png",
                "description": "مدیریت کارها و وظایف",
                "page": "TodoList"
            },
            {
                "name": "فیلدها",
                "icon": "add.png",
                "description": "مدیریت فیلدهای سفارشی",
                "page": "Fields"
            },
            {
                "name": "مسیرهای یادگیری",
                "icon": "stopwatch.png",
                "description": "مدیریت مسیرهای یادگیری",
                "page": "LearningPaths"
            },
            {
                "name": "تایمر",
                "icon": "timer.png",
                "description": "تایمر پومودورو برای مدیریت زمان",
                "page": "Timer"
            },
            {
                "name": "ماشین حساب",
                "icon": "information.png",  # استفاده از آیکون موجود (می‌توانید calculator.png اضافه کنید)
                "description": "ماشین حساب ساده برای محاسبات روزمره",
                "page": "Calculator"
            },
        ]
        
        # ایجاد کارت‌ها
        row = 0
        col = 0
        max_cols = 3
        
        for feature in features:
            card = self.create_feature_card(
                feature["name"],
                feature["icon"],
                feature["description"],
                feature["page"]
            )
            grid.addWidget(card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # اضافه کردن stretch برای فاصله
        layout.addLayout(grid)
        layout.addStretch()
    
    def create_feature_card(self, name, icon_name, description, page_name):
        """ایجاد کارت برای هر امکان"""
        card = QWidget()
        card.setObjectName("feature-card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(10)
        
        # آیکون
        icon_path = os.path.join("icons", icon_name)
        icon_label = QLabel()
        if os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(64, 64))
        else:
            icon_label.setText("📌")
            icon_label.setFont(QFont("Segoe UI", 48))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(icon_label)
        
        # نام
        name_label = QLabel(name)
        name_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(name_label)
        
        # توضیحات
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)
        
        # دکمه باز کردن
        open_btn = QPushButton("باز کردن")
        open_btn.clicked.connect(lambda: self.open_feature(page_name))
        card_layout.addWidget(open_btn)
        
        # استایل کارت
        card.setMinimumSize(200, 250)
        card.setMaximumSize(300, 350)
        
        return card
    
    def open_feature(self, page_name):
        """باز کردن صفحه مربوط به امکان"""
        if self.page_manager:
            self.page_manager.switch_page(page_name)
        else:
            self.feature_clicked.emit(page_name)
    
    def get_current_theme(self):
        """دریافت تم فعلی از config"""
        config_path = "configg/theme_config.txt"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    theme = f.read().strip() or "روشن"
                    return theme == "دارک"
            except Exception:
                return True
        return True
    
    def apply_theme(self):
        """اعمال تم بر اساس config فعلی"""
        is_dark = self.get_current_theme()
        
        if is_dark:
            card_style = """
                QWidget#feature-card {
                    background-color: #2d2d30;
                    border: 1px solid #3e3e42;
                    border-radius: 12px;
                    color: white;
                }
                QWidget#feature-card:hover {
                    background-color: #3e3e42;
                    border-color: #569cd6;
                }
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
                QLabel {
                    color: white;
                }
            """
            page_style = """
                QWidget {
                    background-color: #1e1e1e;
                    color: white;
                }
            """
        else:
            card_style = """
                QWidget#feature-card {
                    background-color: #f1f1f1;
                    border: 1px solid #ddd;
                    border-radius: 12px;
                    color: #1e1e1e;
                }
                QWidget#feature-card:hover {
                    background-color: #e9e9e9;
                    border-color: #0078d7;
                }
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
                QLabel {
                    color: #1e1e1e;
                }
            """
            page_style = """
                QWidget {
                    background-color: #ffffff;
                    color: #1e1e1e;
                }
            """
        
        self.setStyleSheet(page_style + card_style)

