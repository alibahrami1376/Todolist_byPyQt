from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, 
    QMessageBox, QDateEdit, QGroupBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import date
import json
import os


class HabitMotivationPage(QWidget):
    """صفحه انگیزش روزانه"""
    
    def __init__(self):
        super().__init__()
        self.current_date = date.today()
        self.motivation_data = {}
        self.load_motivation_data()
        self.init_ui()
        self.load_today_motivation()
        self.apply_theme()
    
    def showEvent(self, event):
        """وقتی صفحه نمایش داده می‌شود"""
        super().showEvent(event)
        self.load_today_motivation()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # هدر
        header_layout = QHBoxLayout()
        title = QLabel("🌟 انگیزش روزانه")
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
        
        # بخش انگیزش
        motivation_group = QGroupBox("🌟 انگیزش روزانه")
        motivation_layout = QVBoxLayout()
        
        motivation_label = QLabel("چه چیزی امروز را عالی کرد؟")
        motivation_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        motivation_layout.addWidget(motivation_label)
        
        self.motivation_input = QTextEdit()
        self.motivation_input.setPlaceholderText("نوشتن درباره چیزهایی که امروز انجام دادی و به تو انگیزه می‌دهد...")
        self.motivation_input.setMinimumHeight(400)
        motivation_layout.addWidget(self.motivation_input)
        
        # دکمه ذخیره انگیزش
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        save_motivation_btn = QPushButton("💾 ذخیره انگیزش")
        save_motivation_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        save_motivation_btn.clicked.connect(self.save_motivation)
        save_motivation_btn.setMinimumHeight(40)
        btn_layout.addWidget(save_motivation_btn)
        motivation_layout.addLayout(btn_layout)
        
        motivation_group.setLayout(motivation_layout)
        layout.addWidget(motivation_group)
        
        layout.addStretch()
    
    def on_date_changed(self, qdate):
        """وقتی تاریخ تغییر می‌کند"""
        self.current_date = qdate.toPyDate()
        self.load_today_motivation()
    
    def save_motivation(self):
        """ذخیره انگیزش روزانه"""
        date_str = self.current_date.isoformat()
        self.motivation_data[date_str] = self.motivation_input.toPlainText()
        self.save_motivation_data()
        QMessageBox.information(self, "موفق", "انگیزش روزانه ذخیره شد.")
    
    def load_today_motivation(self):
        """بارگذاری انگیزش امروز"""
        date_str = self.current_date.isoformat()
        motivation = self.motivation_data.get(date_str, '')
        self.motivation_input.setPlainText(motivation)
    
    def load_motivation_data(self):
        """بارگذاری داده‌های انگیزش از فایل"""
        motivation_path = os.path.join("data", "motivations.json")
        
        if os.path.exists(motivation_path):
            try:
                with open(motivation_path, 'r', encoding='utf-8') as f:
                    self.motivation_data = json.load(f)
            except:
                self.motivation_data = {}
        else:
            self.motivation_data = {}
    
    def save_motivation_data(self):
        """ذخیره داده‌های انگیزش در فایل"""
        os.makedirs("data", exist_ok=True)
        motivation_path = os.path.join("data", "motivations.json")
        
        with open(motivation_path, 'w', encoding='utf-8') as f:
            json.dump(self.motivation_data, f, ensure_ascii=False, indent=2)
    
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
                QTextEdit, QDateEdit {
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
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
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
                QTextEdit, QDateEdit {
                    background-color: #f1f1f1;
                    color: #1e1e1e;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
            """
        
        self.setStyleSheet(style)

