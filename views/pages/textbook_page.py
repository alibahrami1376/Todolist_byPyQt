from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QDialog, QLineEdit, QTextEdit,
    QComboBox, QHeaderView, QSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from services.textbook_service import TextbookService
from services.course_service import CourseService
from models.db.course_entity import TextbookEntity, CourseEntity


class TextbookDialog(QDialog):
    """دیالوگ برای افزودن/ویرایش کتاب درسی"""
    
    def __init__(self, parent=None, textbook: TextbookEntity = None):
        super().__init__(parent)
        self.textbook = textbook
        self.course_service = CourseService()
        self.setWindowTitle("افزودن کتاب درسی جدید" if not textbook else "ویرایش کتاب درسی")
        self.setMinimumWidth(500)
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # عنوان
        title_label = QLabel("عنوان کتاب:")
        layout.addWidget(title_label)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("مثلاً: Python Crash Course")
        if self.textbook:
            self.title_input.setText(self.textbook.title)
        layout.addWidget(self.title_input)
        
        # محتوا
        content_label = QLabel("محتوا:")
        layout.addWidget(content_label)
        self.content_input = QTextEdit()
        self.content_input.setMaximumHeight(100)
        self.content_input.setPlaceholderText("توضیحات یا یادداشت‌ها...")
        if self.textbook:
            self.content_input.setPlainText(self.textbook.content or "")
        layout.addWidget(self.content_input)
        
        # دوره (اختیاری)
        course_label = QLabel("دوره (اختیاری):")
        layout.addWidget(course_label)
        self.course_combo = QComboBox()
        self.course_combo.addItem("بدون دوره", None)
        try:
            courses = self.course_service.get_all_courses()
            for course in courses:
                self.course_combo.addItem(course.title, course.id)
        except:
            pass
        if self.textbook and self.textbook.course_id:
            index = self.course_combo.findData(self.textbook.course_id)
            if index >= 0:
                self.course_combo.setCurrentIndex(index)
        layout.addWidget(self.course_combo)
        
        # لینک
        link_label = QLabel("لینک:")
        layout.addWidget(link_label)
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("https://...")
        if self.textbook:
            self.link_input.setText(self.textbook.link or "")
        layout.addWidget(self.link_input)
        
        # پیشرفت
        progress_label = QLabel("پیشرفت (%):")
        layout.addWidget(progress_label)
        self.progress_spin = QSpinBox()
        self.progress_spin.setMinimum(0)
        self.progress_spin.setMaximum(100)
        if self.textbook:
            try:
                self.progress_spin.setValue(int(self.textbook.progress))
            except:
                self.progress_spin.setValue(0)
        layout.addWidget(self.progress_spin)
        
        # دکمه‌ها
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("ذخیره")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("لغو")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
    
    def get_textbook_data(self):
        """دریافت داده‌های کتاب درسی"""
        course_id = self.course_combo.currentData()
        return {
            "title": self.title_input.text().strip(),
            "content": self.content_input.toPlainText().strip() or None,
            "course_id": course_id,
            "link": self.link_input.text().strip() or None,
            "progress": float(self.progress_spin.value())
        }
    
    def apply_theme(self):
        from utils.app_config import AppConfig
        is_dark = AppConfig.get_theme() == "دارک"
        
        if is_dark:
            style = """
                QWidget { background-color: #1e1e1e; color: white; }
                QLineEdit, QTextEdit, QComboBox, QSpinBox {
                    background-color: #2d2d30; color: white;
                    border: 1px solid #3e3e42; border-radius: 4px; padding: 6px;
                }
                QPushButton {
                    background-color: #0078d7; color: white;
                    padding: 8px 16px; border-radius: 6px;
                }
                QPushButton:hover { background-color: #005a9e; }
            """
        else:
            style = """
                QWidget { background-color: #ffffff; color: #1e1e1e; }
                QLineEdit, QTextEdit, QComboBox, QSpinBox {
                    background-color: #f1f1f1; color: #1e1e1e;
                    border: 1px solid #ddd; border-radius: 4px; padding: 6px;
                }
                QPushButton {
                    background-color: #0078d7; color: white;
                    padding: 8px 16px; border-radius: 6px;
                }
                QPushButton:hover { background-color: #005a9e; }
            """
        self.setStyleSheet(style)


class TextbookPage(QWidget):
    """صفحه مدیریت کتاب‌های درسی"""
    
    def __init__(self):
        super().__init__()
        self.service = TextbookService()
        self.course_service = CourseService()
        self.init_ui()
        self.load_textbooks()
        self.apply_theme()
    
    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, 'service'):
            self.load_textbooks()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # هدر
        header_layout = QHBoxLayout()
        title = QLabel("📖 مدیریت کتاب‌های درسی")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # دکمه افزودن
        add_btn = QPushButton("➕ افزودن کتاب")
        add_btn.clicked.connect(self.add_textbook)
        header_layout.addWidget(add_btn)
        layout.addLayout(header_layout)
        
        # جدول کتاب‌ها
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "عنوان", "محتوا", "دوره", "لینک", "پیشرفت", "تاریخ ایجاد"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table, 1)
        
        # دکمه‌های عملیات
        btn_layout = QHBoxLayout()
        edit_btn = QPushButton("✏️ ویرایش")
        edit_btn.clicked.connect(self.edit_textbook)
        btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ حذف")
        delete_btn.clicked.connect(self.delete_textbook)
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
    
    def load_textbooks(self):
        """بارگذاری کتاب‌های درسی از دیتابیس"""
        try:
            textbooks = self.service.get_all_textbooks()
            self.table.setRowCount(len(textbooks))
            
            # ایجاد دیکشنری برای نام دوره‌ها
            courses = {c.id: c.title for c in self.course_service.get_all_courses()}
            
            for row, textbook in enumerate(textbooks):
                self.table.setItem(row, 0, QTableWidgetItem(textbook.id))
                self.table.setItem(row, 1, QTableWidgetItem(textbook.title))
                self.table.setItem(row, 2, QTableWidgetItem(textbook.content or ""))
                course_name = courses.get(textbook.course_id, "بدون دوره") if textbook.course_id else "بدون دوره"
                self.table.setItem(row, 3, QTableWidgetItem(course_name))
                self.table.setItem(row, 4, QTableWidgetItem(textbook.link or ""))
                self.table.setItem(row, 5, QTableWidgetItem(f"{int(textbook.progress)}%"))
                self.table.setItem(row, 6, QTableWidgetItem(
                    textbook.created_at.strftime("%Y-%m-%d") if textbook.created_at else ""
                ))
        except Exception as e:
            print(f"خطا در بارگذاری کتاب‌های درسی: {e}")
            QMessageBox.warning(self, "خطا", f"خطا در بارگذاری کتاب‌های درسی: {str(e)}")
    
    def add_textbook(self):
        """افزودن کتاب درسی جدید"""
        dialog = TextbookDialog(self)
        if dialog.exec():
            textbook_data = dialog.get_textbook_data()
            if not textbook_data["title"]:
                QMessageBox.warning(self, "خطا", "لطفاً عنوان کتاب را وارد کنید.")
                return
            try:
                self.service.create_textbook(**textbook_data)
                self.load_textbooks()
                QMessageBox.information(self, "موفق", "کتاب درسی با موفقیت ایجاد شد.")
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ایجاد کتاب درسی: {str(e)}")
    
    def edit_textbook(self):
        """ویرایش کتاب درسی"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک کتاب را انتخاب کنید.")
            return
        
        textbook_id = self.table.item(selected, 0).text()
        textbook = self.service.get_textbook_by_id(textbook_id)
        if not textbook:
            QMessageBox.warning(self, "خطا", "کتاب یافت نشد.")
            return
        
        dialog = TextbookDialog(self, textbook)
        if dialog.exec():
            textbook_data = dialog.get_textbook_data()
            if not textbook_data["title"]:
                QMessageBox.warning(self, "خطا", "لطفاً عنوان کتاب را وارد کنید.")
                return
            try:
                if self.service.update_textbook(textbook_id, **textbook_data):
                    self.load_textbooks()
                    QMessageBox.information(self, "موفق", "کتاب درسی با موفقیت به‌روزرسانی شد.")
                else:
                    QMessageBox.warning(self, "خطا", "کتاب یافت نشد.")
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ویرایش کتاب درسی: {str(e)}")
    
    def delete_textbook(self):
        """حذف کتاب درسی"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک کتاب را انتخاب کنید.")
            return
        
        textbook_id = self.table.item(selected, 0).text()
        textbook_title = self.table.item(selected, 1).text()
        
        reply = QMessageBox.question(
            self, "حذف کتاب",
            f"آیا مطمئن هستید که می‌خواهید کتاب '{textbook_title}' را حذف کنید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.service.delete_textbook(textbook_id):
                    self.load_textbooks()
                    QMessageBox.information(self, "موفق", "کتاب درسی با موفقیت حذف شد.")
                else:
                    QMessageBox.warning(self, "خطا", "کتاب یافت نشد.")
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در حذف کتاب درسی: {str(e)}")
    
    def apply_theme(self):
        from utils.app_config import AppConfig
        is_dark = AppConfig.get_theme() == "دارک"
        
        if is_dark:
            style = """
                QWidget { background-color: #1e1e1e; color: white; }
                QPushButton {
                    background-color: #0078d7; color: white;
                    padding: 8px 16px; border-radius: 6px;
                }
                QPushButton:hover { background-color: #005a9e; }
                QTableWidget {
                    background-color: #2d2d30; color: white;
                    border: 1px solid #3e3e42; border-radius: 8px;
                }
                QTableWidget::item { padding: 5px; }
                QTableWidget::item:selected {
                    background-color: #0078d7;
                }
                QHeaderView::section {
                    background-color: #3e3e42; color: white;
                    padding: 8px; border: none;
                }
            """
        else:
            style = """
                QWidget { background-color: #ffffff; color: #1e1e1e; }
                QPushButton {
                    background-color: #0078d7; color: white;
                    padding: 8px 16px; border-radius: 6px;
                }
                QPushButton:hover { background-color: #005a9e; }
                QTableWidget {
                    background-color: #f1f1f1; color: #1e1e1e;
                    border: 1px solid #ddd; border-radius: 8px;
                }
                QTableWidget::item { padding: 5px; }
                QTableWidget::item:selected {
                    background-color: #0078d7; color: white;
                }
                QHeaderView::section {
                    background-color: #e9e9e9; color: #1e1e1e;
                    padding: 8px; border: none;
                }
            """
        self.setStyleSheet(style)

