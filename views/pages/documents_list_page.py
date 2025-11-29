from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from services.document_service import DocumentService
from services.course_service import CourseService
from services.textbook_service import TextbookService
from views.pages.document_editor_page import DocumentEditorPage


class DocumentsListPage(QWidget):
    """صفحه لیست سندها"""
    
    def __init__(self, page_manager=None):
        super().__init__()
        self.page_manager = page_manager
        self.service = DocumentService()
        self.course_service = CourseService()
        self.textbook_service = TextbookService()
        self.init_ui()
        self.load_documents()
        self.apply_theme()
    
    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, 'service'):
            self.load_documents()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # هدر
        header_layout = QHBoxLayout()
        title = QLabel("📄 مدیریت سندها")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # دکمه ایجاد سند جدید
        new_doc_btn = QPushButton("➕ سند جدید")
        new_doc_btn.clicked.connect(self.create_new_document)
        header_layout.addWidget(new_doc_btn)
        
        layout.addLayout(header_layout)
        
        # جدول سندها
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "عنوان", "دوره", "کتاب", "تاریخ به‌روزرسانی"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self.open_document)
        layout.addWidget(self.table, 1)
        
        # دکمه‌های عملیات
        btn_layout = QHBoxLayout()
        
        open_btn = QPushButton("📖 باز کردن")
        open_btn.clicked.connect(self.open_document)
        btn_layout.addWidget(open_btn)
        
        delete_btn = QPushButton("🗑️ حذف")
        delete_btn.clicked.connect(self.delete_document)
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
    
    def load_documents(self):
        """بارگذاری سندها از دیتابیس"""
        try:
            documents = self.service.get_all_documents()
            self.table.setRowCount(len(documents))
            
            # ایجاد دیکشنری برای نام دوره‌ها و کتاب‌ها
            courses = {c.id: c.title for c in self.course_service.get_all_courses()}
            textbooks = {t.id: t.title for t in self.textbook_service.get_all_textbooks()}
            
            for row, document in enumerate(documents):
                self.table.setItem(row, 0, QTableWidgetItem(document.id))
                self.table.setItem(row, 1, QTableWidgetItem(document.title))
                
                course_name = courses.get(document.course_id, "بدون دوره") if document.course_id else "بدون دوره"
                self.table.setItem(row, 2, QTableWidgetItem(course_name))
                
                textbook_name = textbooks.get(document.textbook_id, "بدون کتاب") if document.textbook_id else "بدون کتاب"
                self.table.setItem(row, 3, QTableWidgetItem(textbook_name))
                
                self.table.setItem(row, 4, QTableWidgetItem(
                    document.updated_at.strftime("%Y-%m-%d %H:%M") if document.updated_at else ""
                ))
        except Exception as e:
            print(f"خطا در بارگذاری سندها: {e}")
            QMessageBox.warning(self, "خطا", f"خطا در بارگذاری سندها: {str(e)}")
    
    def create_new_document(self):
        """ایجاد سند جدید"""
        if self.page_manager:
            # ایجاد صفحه ویرایشگر با سند جدید
            editor = DocumentEditorPage()
            self.page_manager.add_page(editor, f"DocumentEditor_{editor.document_id}")
            self.page_manager.switch_page(f"DocumentEditor_{editor.document_id}")
    
    def open_document(self):
        """باز کردن سند"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک سند را انتخاب کنید.")
            return
        
        document_id = self.table.item(selected, 0).text()
        
        if self.page_manager:
            # ایجاد صفحه ویرایشگر با سند موجود
            editor = DocumentEditorPage(document_id=document_id)
            self.page_manager.add_page(editor, f"DocumentEditor_{document_id}")
            self.page_manager.switch_page(f"DocumentEditor_{document_id}")
    
    def delete_document(self):
        """حذف سند"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک سند را انتخاب کنید.")
            return
        
        document_id = self.table.item(selected, 0).text()
        document_title = self.table.item(selected, 1).text()
        
        reply = QMessageBox.question(
            self, "حذف سند",
            f"آیا مطمئن هستید که می‌خواهید سند '{document_title}' را حذف کنید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.service.delete_document(document_id):
                    self.load_documents()
                    QMessageBox.information(self, "موفق", "سند با موفقیت حذف شد.")
                else:
                    QMessageBox.warning(self, "خطا", "سند یافت نشد.")
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در حذف سند: {str(e)}")
    
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

