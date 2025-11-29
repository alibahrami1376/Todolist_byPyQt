from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QDialog, QLineEdit, QTextEdit, QDateEdit,
    QComboBox, QHeaderView
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import date
from services.course_service import CourseService
from models.db.course_entity import CourseEntity


class CourseDialog(QDialog):
    """دیالوگ برای افزودن/ویرایش دوره"""
    
    def __init__(self, parent=None, course: CourseEntity = None):
        super().__init__(parent)
        self.course = course
        self.setWindowTitle("افزودن دوره جدید" if not course else "ویرایش دوره")
        self.setMinimumWidth(500)
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # عنوان
        title_label = QLabel("عنوان دوره:")
        layout.addWidget(title_label)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("مثلاً: Python Programming")
        if self.course:
            self.title_input.setText(self.course.title)
        layout.addWidget(self.title_input)
        
        # توضیحات
        desc_label = QLabel("توضیحات:")
        layout.addWidget(desc_label)
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        self.desc_input.setPlaceholderText("توضیحات دوره...")
        if self.course:
            self.desc_input.setPlainText(self.course.description or "")
        layout.addWidget(self.desc_input)
        
        # تاریخ شروع
        date_label = QLabel("تاریخ شروع:")
        layout.addWidget(date_label)
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        if self.course and self.course.start_date:
            self.date_input.setDate(QDate(self.course.start_date.year, self.course.start_date.month, self.course.start_date.day))
        layout.addWidget(self.date_input)
        
        # لینک
        link_label = QLabel("لینک:")
        layout.addWidget(link_label)
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("https://...")
        if self.course:
            self.link_input.setText(self.course.link or "")
        layout.addWidget(self.link_input)
        
        # وضعیت
        status_label = QLabel("وضعیت:")
        layout.addWidget(status_label)
        self.status_combo = QComboBox()
        self.status_combo.addItems(["در حال انجام", "تکمیل شده", "متوقف شده"])
        if self.course:
            index = self.status_combo.findText(self.course.status)
            if index >= 0:
                self.status_combo.setCurrentIndex(index)
        layout.addWidget(self.status_combo)
        
        # دکمه‌ها
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("ذخیره")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("لغو")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
    
    def get_course_data(self):
        """دریافت داده‌های دوره"""
        return {
            "title": self.title_input.text().strip(),
            "description": self.desc_input.toPlainText().strip() or None,
            "start_date": self.date_input.date().toPyDate(),
            "link": self.link_input.text().strip() or None,
            "status": self.status_combo.currentText()
        }
    
    def apply_theme(self):
        from utils.app_config import AppConfig
        is_dark = AppConfig.get_theme() == "دارک"
        
        if is_dark:
            style = """
                QWidget { background-color: #1e1e1e; color: white; }
                QLineEdit, QTextEdit, QComboBox, QDateEdit {
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
                QLineEdit, QTextEdit, QComboBox, QDateEdit {
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


class CoursePage(QWidget):
    """صفحه مدیریت دوره‌ها"""
    
    def __init__(self):
        super().__init__()
        self.service = CourseService()
        self.init_ui()
        self.load_courses()
        self.apply_theme()
    
    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, 'service'):
            self.load_courses()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # هدر
        header_layout = QHBoxLayout()
        title = QLabel("📚 مدیریت دوره‌ها")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # دکمه افزودن
        add_btn = QPushButton("➕ افزودن دوره")
        add_btn.clicked.connect(self.add_course)
        header_layout.addWidget(add_btn)
        layout.addLayout(header_layout)
        
        # جدول دوره‌ها
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "عنوان", "توضیحات", "تاریخ شروع", "لینک", "وضعیت"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table, 1)
        
        # دکمه‌های عملیات
        btn_layout = QHBoxLayout()
        edit_btn = QPushButton("✏️ ویرایش")
        edit_btn.clicked.connect(self.edit_course)
        btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ حذف")
        delete_btn.clicked.connect(self.delete_course)
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
    
    def load_courses(self):
        """بارگذاری دوره‌ها از دیتابیس"""
        try:
            courses = self.service.get_all_courses()
            self.table.setRowCount(len(courses))
            
            for row, course in enumerate(courses):
                self.table.setItem(row, 0, QTableWidgetItem(course.id))
                self.table.setItem(row, 1, QTableWidgetItem(course.title))
                self.table.setItem(row, 2, QTableWidgetItem(course.description or ""))
                self.table.setItem(row, 3, QTableWidgetItem(
                    course.start_date.strftime("%Y-%m-%d") if course.start_date else ""
                ))
                self.table.setItem(row, 4, QTableWidgetItem(course.link or ""))
                self.table.setItem(row, 5, QTableWidgetItem(course.status))
        except Exception as e:
            print(f"خطا در بارگذاری دوره‌ها: {e}")
            QMessageBox.warning(self, "خطا", f"خطا در بارگذاری دوره‌ها: {str(e)}")
    
    def add_course(self):
        """افزودن دوره جدید"""
        dialog = CourseDialog(self)
        if dialog.exec():
            course_data = dialog.get_course_data()
            if not course_data["title"]:
                QMessageBox.warning(self, "خطا", "لطفاً عنوان دوره را وارد کنید.")
                return
            try:
                self.service.create_course(**course_data)
                self.load_courses()
                QMessageBox.information(self, "موفق", "دوره با موفقیت ایجاد شد.")
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ایجاد دوره: {str(e)}")
    
    def edit_course(self):
        """ویرایش دوره"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک دوره را انتخاب کنید.")
            return
        
        course_id = self.table.item(selected, 0).text()
        course = self.service.get_course_by_id(course_id)
        if not course:
            QMessageBox.warning(self, "خطا", "دوره یافت نشد.")
            return
        
        dialog = CourseDialog(self, course)
        if dialog.exec():
            course_data = dialog.get_course_data()
            if not course_data["title"]:
                QMessageBox.warning(self, "خطا", "لطفاً عنوان دوره را وارد کنید.")
                return
            try:
                if self.service.update_course(course_id, **course_data):
                    self.load_courses()
                    QMessageBox.information(self, "موفق", "دوره با موفقیت به‌روزرسانی شد.")
                else:
                    QMessageBox.warning(self, "خطا", "دوره یافت نشد.")
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ویرایش دوره: {str(e)}")
    
    def delete_course(self):
        """حذف دوره"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک دوره را انتخاب کنید.")
            return
        
        course_id = self.table.item(selected, 0).text()
        course_title = self.table.item(selected, 1).text()
        
        reply = QMessageBox.question(
            self, "حذف دوره",
            f"آیا مطمئن هستید که می‌خواهید دوره '{course_title}' را حذف کنید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.service.delete_course(course_id):
                    self.load_courses()
                    QMessageBox.information(self, "موفق", "دوره با موفقیت حذف شد.")
                else:
                    QMessageBox.warning(self, "خطا", "دوره یافت نشد.")
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در حذف دوره: {str(e)}")
    
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

