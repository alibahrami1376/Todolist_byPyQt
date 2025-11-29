from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, 
    QMessageBox, QDateEdit, QGroupBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import date
import json
import os


class HabitReflectionPage(QWidget):
    """صفحه بازتاب روزانه"""
    
    def __init__(self):
        super().__init__()
        self.current_date = date.today()
        self.reflection_data = {}
        self.load_reflection_data()
        self.init_ui()
        self.load_today_reflection()
        self.apply_theme()
    
    def showEvent(self, event):
        """وقتی صفحه نمایش داده می‌شود"""
        super().showEvent(event)
        self.load_today_reflection()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # هدر
        header_layout = QHBoxLayout()
        title = QLabel("💭 بازتاب روزانه")
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
        
        # بخش بازتاب
        reflection_group = QGroupBox("💭 بازتاب روزانه")
        reflection_layout = QVBoxLayout()
        
        # بهترین لحظات روز
        best_moments_label = QLabel("بهترین لحظات امروز:")
        best_moments_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        reflection_layout.addWidget(best_moments_label)
        self.best_moments_input = QTextEdit()
        self.best_moments_input.setPlaceholderText("چه چیزهایی امروز را خاص کرد؟")
        self.best_moments_input.setMinimumHeight(100)
        reflection_layout.addWidget(self.best_moments_input)
        
        # چه چیزهایی خوب پیش رفت
        went_well_label = QLabel("چه چیزهایی خوب پیش رفت:")
        went_well_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        reflection_layout.addWidget(went_well_label)
        self.went_well_input = QTextEdit()
        self.went_well_input.setPlaceholderText("چه کارهایی را امروز به خوبی انجام دادی؟")
        self.went_well_input.setMinimumHeight(100)
        reflection_layout.addWidget(self.went_well_input)
        
        # چیزهایی برای بهبود
        improve_label = QLabel("چیزهایی برای بهبود:")
        improve_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        reflection_layout.addWidget(improve_label)
        self.improve_input = QTextEdit()
        self.improve_input.setPlaceholderText("چه چیزهایی را می‌توانی بهتر کنی؟")
        self.improve_input.setMinimumHeight(100)
        reflection_layout.addWidget(self.improve_input)
        
        # دکمه ذخیره بازتاب
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        save_reflection_btn = QPushButton("💾 ذخیره بازتاب")
        save_reflection_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        save_reflection_btn.clicked.connect(self.save_reflection)
        save_reflection_btn.setMinimumHeight(40)
        btn_layout.addWidget(save_reflection_btn)
        reflection_layout.addLayout(btn_layout)
        
        reflection_group.setLayout(reflection_layout)
        layout.addWidget(reflection_group)
        
        layout.addStretch()
    
    def on_date_changed(self, qdate):
        """وقتی تاریخ تغییر می‌کند"""
        self.current_date = qdate.toPyDate()
        self.load_today_reflection()
    
    def save_reflection(self):
        """ذخیره بازتاب روزانه"""
        date_str = self.current_date.isoformat()
        self.reflection_data[date_str] = {
            'best_moments': self.best_moments_input.toPlainText(),
            'went_well': self.went_well_input.toPlainText(),
            'improve': self.improve_input.toPlainText()
        }
        self.save_reflection_data()
        QMessageBox.information(self, "موفق", "بازتاب روزانه ذخیره شد.")
    
    def load_today_reflection(self):
        """بارگذاری بازتاب امروز"""
        date_str = self.current_date.isoformat()
        reflection = self.reflection_data.get(date_str, {})
        self.best_moments_input.setPlainText(reflection.get('best_moments', ''))
        self.went_well_input.setPlainText(reflection.get('went_well', ''))
        self.improve_input.setPlainText(reflection.get('improve', ''))
    
    def load_reflection_data(self):
        """بارگذاری داده‌های بازتاب از فایل"""
        reflection_path = os.path.join("data", "reflections.json")
        
        if os.path.exists(reflection_path):
            try:
                with open(reflection_path, 'r', encoding='utf-8') as f:
                    self.reflection_data = json.load(f)
            except:
                self.reflection_data = {}
        else:
            self.reflection_data = {}
    
    def save_reflection_data(self):
        """ذخیره داده‌های بازتاب در فایل"""
        os.makedirs("data", exist_ok=True)
        reflection_path = os.path.join("data", "reflections.json")
        
        with open(reflection_path, 'w', encoding='utf-8') as f:
            json.dump(self.reflection_data, f, ensure_ascii=False, indent=2)
    
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

