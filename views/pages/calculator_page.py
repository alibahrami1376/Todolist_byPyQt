from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import os


class CalculatorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.current = "0"
        self.previous = None
        self.operation = None
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # نمایشگر
        self.display = QLineEdit()
        self.display.setText("0")
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setMinimumHeight(70)
        layout.addWidget(self.display)
        
        # Grid برای دکمه‌ها
        grid = QGridLayout()
        grid.setSpacing(10)
        
        # دکمه‌های ماشین حساب
        buttons = [
            ('C', 0, 0), ('CE', 0, 1), ('⌫', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('±', 4, 0), ('0', 4, 1), ('.', 4, 2), ('=', 4, 3),
        ]
        
        for (text, row, col) in buttons:
            btn = self.create_button(text)
            grid.addWidget(btn, row, col)
        
        layout.addLayout(grid)
        layout.addStretch()
    
    def create_button(self, text):
        """ایجاد دکمه با استایل مناسب"""
        btn = QPushButton(text)
        btn.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        btn.setMinimumHeight(60)
        
        # استایل بر اساس نوع دکمه
        if text in ['C', 'CE', '⌫']:
            btn.setObjectName("clear-button")
        elif text in ['÷', '×', '-', '+', '=']:
            btn.setObjectName("operator-button")
        elif text == '±':
            btn.setObjectName("special-button")
        else:
            btn.setObjectName("number-button")
        
        btn.clicked.connect(lambda: self.button_clicked(text))
        return btn
    
    def button_clicked(self, text):
        """مدیریت کلیک دکمه‌ها"""
        if text.isdigit() or text == '.':
            self.number_clicked(text)
        elif text in ['÷', '×', '-', '+']:
            self.operator_clicked(text)
        elif text == '=':
            self.equals_clicked()
        elif text == 'C':
            self.clear_all()
        elif text == 'CE':
            self.clear_entry()
        elif text == '⌫':
            self.backspace()
        elif text == '±':
            self.toggle_sign()
    
    def number_clicked(self, digit):
        """اضافه کردن عدد به نمایشگر"""
        if self.current == "0" and digit != '.':
            self.current = digit
        else:
            if digit == '.' and '.' in self.current:
                return  # جلوگیری از اضافه کردن نقطه تکراری
            self.current += digit
        self.update_display()
    
    def operator_clicked(self, op):
        """مدیریت عملگرها"""
        if self.previous is None:
            self.previous = float(self.current)
        else:
            self.calculate()
        
        # تبدیل نمادهای نمایشی به عملگرهای پایتون
        op_map = {'÷': '/', '×': '*', '-': '-', '+': '+'}
        self.operation = op_map[op]
        self.current = "0"
    
    def equals_clicked(self):
        """محاسبه نتیجه"""
        if self.previous is not None and self.operation:
            self.calculate()
            self.operation = None
            self.previous = None
    
    def calculate(self):
        """انجام محاسبه"""
        try:
            current_num = float(self.current)
            if self.operation == '/':
                if current_num == 0:
                    self.current = "خطا"
                    self.previous = None
                    return
                result = self.previous / current_num
            elif self.operation == '*':
                result = self.previous * current_num
            elif self.operation == '-':
                result = self.previous - current_num
            elif self.operation == '+':
                result = self.previous + current_num
            else:
                return
            
            # نمایش نتیجه به صورت عدد صحیح اگر اعشار ندارد
            if result.is_integer():
                self.current = str(int(result))
            else:
                self.current = str(result)
            
            self.previous = result
            self.update_display()
        except Exception:
            self.current = "خطا"
            self.update_display()
    
    def clear_all(self):
        """پاک کردن همه"""
        self.current = "0"
        self.previous = None
        self.operation = None
        self.update_display()
    
    def clear_entry(self):
        """پاک کردن ورودی فعلی"""
        self.current = "0"
        self.update_display()
    
    def backspace(self):
        """حذف آخرین کاراکتر"""
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"
        self.update_display()
    
    def toggle_sign(self):
        """تغییر علامت"""
        try:
            num = float(self.current)
            num = -num
            if num.is_integer():
                self.current = str(int(num))
            else:
                self.current = str(num)
            self.update_display()
        except Exception:
            pass
    
    def update_display(self):
        """به‌روزرسانی نمایشگر"""
        self.display.setText(self.current)
    
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
            style = """
                QWidget {
                    background-color: #1e1e1e;
                    color: white;
                }
                QLineEdit {
                    background-color: #2d2d30;
                    color: white;
                    border: 2px solid #3e3e42;
                    border-radius: 8px;
                    padding: 10px;
                }
                QPushButton#number-button {
                    background-color: #3e3e42;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton#number-button:hover {
                    background-color: #4e4e52;
                }
                QPushButton#number-button:pressed {
                    background-color: #2e2e32;
                }
                QPushButton#operator-button {
                    background-color: #0078d7;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton#operator-button:hover {
                    background-color: #005a9e;
                }
                QPushButton#operator-button:pressed {
                    background-color: #004578;
                }
                QPushButton#clear-button {
                    background-color: #d13438;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton#clear-button:hover {
                    background-color: #a4262c;
                }
                QPushButton#clear-button:pressed {
                    background-color: #8b1e22;
                }
                QPushButton#special-button {
                    background-color: #3e3e42;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton#special-button:hover {
                    background-color: #4e4e52;
                }
            """
        else:
            style = """
                QWidget {
                    background-color: #ffffff;
                    color: #1e1e1e;
                }
                QLineEdit {
                    background-color: #f1f1f1;
                    color: #1e1e1e;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    padding: 10px;
                }
                QPushButton#number-button {
                    background-color: #e9e9e9;
                    color: #1e1e1e;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton#number-button:hover {
                    background-color: #dcdcdc;
                }
                QPushButton#number-button:pressed {
                    background-color: #c0c0c0;
                }
                QPushButton#operator-button {
                    background-color: #0078d7;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton#operator-button:hover {
                    background-color: #005a9e;
                }
                QPushButton#operator-button:pressed {
                    background-color: #004578;
                }
                QPushButton#clear-button {
                    background-color: #d13438;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton#clear-button:hover {
                    background-color: #a4262c;
                }
                QPushButton#clear-button:pressed {
                    background-color: #8b1e22;
                }
                QPushButton#special-button {
                    background-color: #e9e9e9;
                    color: #1e1e1e;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton#special-button:hover {
                    background-color: #dcdcdc;
                }
            """
        
        self.setStyleSheet(style)

