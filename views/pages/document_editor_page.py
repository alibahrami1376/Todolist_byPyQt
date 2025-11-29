from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit,
    QLineEdit, QComboBox, QListWidget, QListWidgetItem, QMessageBox,
    QFileDialog, QScrollArea, QFrame, QMenu, QInputDialog
)
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal, QPoint
from PyQt6.QtGui import QFont, QDrag, QPixmap, QPainter, QColor
from services.document_service import DocumentService
from services.course_service import CourseService
from services.textbook_service import TextbookService
from models.db.document_entity import DocumentEntity, DocumentBlockEntity
import json


class BlockWidget(QFrame):
    """ویجت برای نمایش یک بلوک"""
    block_changed = pyqtSignal(str, str, str)  # block_id, block_type, content
    block_deleted = pyqtSignal(str)  # block_id
    block_moved = pyqtSignal(str, int)  # block_id, direction (-1 up, 1 down)
    
    def __init__(self, block: DocumentBlockEntity, parent=None):
        super().__init__(parent)
        self.block = block
        self.block_id = block.id
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)
        
        # هدر بلوک با دکمه‌ها
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # دکمه نوع بلوک
        self.type_btn = QPushButton(self.get_type_label())
        self.type_btn.setMaximumWidth(100)
        self.type_btn.clicked.connect(self.change_type)
        header_layout.addWidget(self.type_btn)
        
        header_layout.addStretch()
        
        # دکمه‌های جابه‌جایی
        up_btn = QPushButton("↑")
        up_btn.setMaximumWidth(30)
        up_btn.clicked.connect(lambda: self.block_moved.emit(self.block_id, -1))
        header_layout.addWidget(up_btn)
        
        down_btn = QPushButton("↓")
        down_btn.setMaximumWidth(30)
        down_btn.clicked.connect(lambda: self.block_moved.emit(self.block_id, 1))
        header_layout.addWidget(down_btn)
        
        # دکمه حذف
        delete_btn = QPushButton("🗑️")
        delete_btn.setMaximumWidth(30)
        delete_btn.clicked.connect(lambda: self.block_deleted.emit(self.block_id))
        header_layout.addWidget(delete_btn)
        
        layout.addLayout(header_layout)
        
        # محتوای بلوک
        self.content_widget = self.create_content_widget()
        layout.addWidget(self.content_widget)
        
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)
    
    def create_content_widget(self):
        """ایجاد ویجت محتوا بر اساس نوع بلوک"""
        block_type = self.block.block_type
        
        if block_type in ["heading1", "heading2", "heading3"]:
            widget = QLineEdit()
            widget.setText(self.block.content or "")
            widget.setPlaceholderText("عنوان را وارد کنید...")
            size = {"heading1": 24, "heading2": 20, "heading3": 16}[block_type]
            font = QFont("Segoe UI", size, QFont.Weight.Bold)
            widget.setFont(font)
            widget.textChanged.connect(self.on_content_changed)
            return widget
        
        elif block_type == "code":
            widget = QTextEdit()
            widget.setPlainText(self.block.content or "")
            widget.setPlaceholderText("کد را وارد کنید...")
            font = QFont("Consolas", 10)
            widget.setFont(font)
            widget.setMaximumHeight(300)
            widget.textChanged.connect(self.on_content_changed)
            return widget
        
        elif block_type == "image":
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
            
            image_label = QLabel()
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setMinimumHeight(200)
            image_label.setStyleSheet("background-color: #f0f0f0; border: 2px dashed #ccc;")
            
            if self.block.block_metadata:
                try:
                    metadata = json.loads(self.block.block_metadata)
                    image_path = metadata.get("path", "")
                    if image_path:
                        pixmap = QPixmap(image_path)
                        if not pixmap.isNull():
                            image_label.setPixmap(pixmap.scaled(400, 200, Qt.AspectRatioMode.KeepAspectRatio))
                except:
                    pass
            
            if image_label.pixmap() is None:
                image_label.setText("برای افزودن عکس کلیک کنید")
                image_label.mousePressEvent = lambda e: self.select_image()
            
            layout.addWidget(image_label)
            
            path_label = QLabel(self.block.content or "")
            path_label.setWordWrap(True)
            layout.addWidget(path_label)
            
            return widget
        
        else:  # text
            widget = QTextEdit()
            widget.setPlainText(self.block.content or "")
            widget.setPlaceholderText("متن را وارد کنید...")
            widget.setMaximumHeight(200)
            widget.textChanged.connect(self.on_content_changed)
            return widget
    
    def get_type_label(self):
        """برچسب نوع بلوک"""
        labels = {
            "text": "📝 متن",
            "heading1": "H1",
            "heading2": "H2",
            "heading3": "H3",
            "code": "💻 کد",
            "image": "🖼️ عکس",
            "list": "📋 لیست"
        }
        return labels.get(self.block.block_type, "📝 متن")
    
    def change_type(self):
        """تغییر نوع بلوک"""
        types = ["text", "heading1", "heading2", "heading3", "code", "image"]
        current_index = types.index(self.block.block_type) if self.block.block_type in types else 0
        
        new_type, ok = QInputDialog.getItem(
            self, "تغییر نوع بلوک", "نوع جدید را انتخاب کنید:",
            ["📝 متن", "H1", "H2", "H3", "💻 کد", "🖼️ عکس"],
            current_index, False
        )
        
        if ok:
            type_map = {
                "📝 متن": "text",
                "H1": "heading1",
                "H2": "heading2",
                "H3": "heading3",
                "💻 کد": "code",
                "🖼️ عکس": "image"
            }
            new_type_key = type_map.get(new_type, "text")
            self.block.block_type = new_type_key
            self.type_btn.setText(new_type)
            self.block_changed.emit(self.block_id, new_type_key, self.get_content())
    
    def select_image(self):
        """انتخاب عکس"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "انتخاب عکس", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            metadata = json.dumps({"path": file_path})
            self.block.block_metadata = metadata
            self.block.content = file_path
            self.block_changed.emit(self.block_id, "image", file_path)
            # بازسازی ویجت
            self.content_widget.deleteLater()
            self.content_widget = self.create_content_widget()
            self.layout().addWidget(self.content_widget)
    
    def get_content(self):
        """دریافت محتوای بلوک"""
        if isinstance(self.content_widget, QLineEdit):
            return self.content_widget.text()
        elif isinstance(self.content_widget, QTextEdit):
            return self.content_widget.toPlainText()
        else:
            return self.block.content or ""
    
    def on_content_changed(self):
        """وقتی محتوا تغییر می‌کند"""
        content = self.get_content()
        self.block_changed.emit(self.block_id, self.block.block_type, content)
    
    def apply_theme(self):
        from utils.app_config import AppConfig
        is_dark = AppConfig.get_theme() == "دارک"
        
        if is_dark:
            self.setStyleSheet("""
                QFrame {
                    background-color: #2d2d30;
                    border: 1px solid #3e3e42;
                    border-radius: 4px;
                    margin: 5px;
                }
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #ffffff;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    margin: 5px;
                }
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
            """)


class DocumentEditorPage(QWidget):
    """صفحه ویرایشگر سند"""
    
    def __init__(self, document_id: str = None):
        super().__init__()
        self.document_id = document_id
        self.service = DocumentService()
        self.course_service = CourseService()
        self.textbook_service = TextbookService()
        self.blocks_widgets = {}  # block_id -> BlockWidget
        self.init_ui()
        self.load_document()
        self.apply_theme()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # هدر
        header_layout = QHBoxLayout()
        
        # عنوان سند
        title_label = QLabel("عنوان سند:")
        header_layout.addWidget(title_label)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("عنوان سند را وارد کنید...")
        self.title_input.textChanged.connect(self.on_title_changed)
        header_layout.addWidget(self.title_input, 1)
        
        # انتخاب دوره (اختیاری)
        course_label = QLabel("دوره:")
        header_layout.addWidget(course_label)
        self.course_combo = QComboBox()
        self.course_combo.addItem("بدون دوره", None)
        try:
            courses = self.course_service.get_all_courses()
            for course in courses:
                self.course_combo.addItem(course.title, course.id)
        except:
            pass
        self.course_combo.currentIndexChanged.connect(self.on_course_changed)
        header_layout.addWidget(self.course_combo)
        
        # انتخاب کتاب (اختیاری)
        textbook_label = QLabel("کتاب:")
        header_layout.addWidget(textbook_label)
        self.textbook_combo = QComboBox()
        self.textbook_combo.addItem("بدون کتاب", None)
        self.textbook_combo.currentIndexChanged.connect(self.on_textbook_changed)
        header_layout.addWidget(self.textbook_combo)
        
        # دکمه ذخیره
        save_btn = QPushButton("💾 ذخیره")
        save_btn.clicked.connect(self.save_document)
        header_layout.addWidget(save_btn)
        
        layout.addLayout(header_layout)
        
        # دکمه‌های افزودن بلوک
        block_buttons_layout = QHBoxLayout()
        
        add_text_btn = QPushButton("➕ متن")
        add_text_btn.clicked.connect(lambda: self.add_block("text"))
        block_buttons_layout.addWidget(add_text_btn)
        
        add_h1_btn = QPushButton("➕ H1")
        add_h1_btn.clicked.connect(lambda: self.add_block("heading1"))
        block_buttons_layout.addWidget(add_h1_btn)
        
        add_h2_btn = QPushButton("➕ H2")
        add_h2_btn.clicked.connect(lambda: self.add_block("heading2"))
        block_buttons_layout.addWidget(add_h2_btn)
        
        add_h3_btn = QPushButton("➕ H3")
        add_h3_btn.clicked.connect(lambda: self.add_block("heading3"))
        block_buttons_layout.addWidget(add_h3_btn)
        
        add_code_btn = QPushButton("➕ کد")
        add_code_btn.clicked.connect(lambda: self.add_block("code"))
        block_buttons_layout.addWidget(add_code_btn)
        
        add_image_btn = QPushButton("➕ عکس")
        add_image_btn.clicked.connect(lambda: self.add_block("image"))
        block_buttons_layout.addWidget(add_image_btn)
        
        block_buttons_layout.addStretch()
        layout.addLayout(block_buttons_layout)
        
        # ناحیه اسکرول برای بلوک‌ها
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.blocks_container = QWidget()
        self.blocks_layout = QVBoxLayout(self.blocks_container)
        self.blocks_layout.setContentsMargins(0, 0, 0, 0)
        self.blocks_layout.setSpacing(10)
        self.blocks_layout.addStretch()
        
        scroll.setWidget(self.blocks_container)
        layout.addWidget(scroll, 1)
    
    def load_document(self):
        """بارگذاری سند"""
        if not self.document_id:
            # ایجاد سند جدید
            self.document_id = self.service.create_document("سند جدید")
        
        document = self.service.get_document_by_id(self.document_id)
        if document:
            self.title_input.setText(document.title)
            
            # تنظیم دوره
            if document.course_id:
                index = self.course_combo.findData(document.course_id)
                if index >= 0:
                    self.course_combo.setCurrentIndex(index)
            
            # تنظیم کتاب
            if document.textbook_id:
                self.update_textbook_combo(document.course_id)
                index = self.textbook_combo.findData(document.textbook_id)
                if index >= 0:
                    self.textbook_combo.setCurrentIndex(index)
            
            # بارگذاری بلوک‌ها
            blocks = self.service.get_document_blocks(self.document_id)
            for block in blocks:
                self.add_block_widget(block)
    
    def update_textbook_combo(self, course_id):
        """به‌روزرسانی لیست کتاب‌ها بر اساس دوره"""
        self.textbook_combo.clear()
        self.textbook_combo.addItem("بدون کتاب", None)
        
        if course_id:
            try:
                textbooks = self.textbook_service.get_all_textbooks(course_id=course_id)
                for textbook in textbooks:
                    self.textbook_combo.addItem(textbook.title, textbook.id)
            except:
                pass
    
    def on_course_changed(self):
        """وقتی دوره تغییر می‌کند"""
        course_id = self.course_combo.currentData()
        self.update_textbook_combo(course_id)
        self.save_document()
    
    def on_textbook_changed(self):
        """وقتی کتاب تغییر می‌کند"""
        self.save_document()
    
    def on_title_changed(self):
        """وقتی عنوان تغییر می‌کند"""
        # ذخیره خودکار بعد از 2 ثانیه (می‌توانید timer اضافه کنید)
        pass
    
    def add_block(self, block_type: str):
        """افزودن بلوک جدید"""
        if not self.document_id:
            self.document_id = self.service.create_document(
                self.title_input.text() or "سند جدید"
            )
        
        blocks = self.service.get_document_blocks(self.document_id)
        order_index = len(blocks)
        
        block_id = self.service.create_block(
            self.document_id,
            block_type,
            "",
            order_index
        )
        
        # بارگذاری بلوک از دیتابیس
        new_block = self.service.get_block_by_id(block_id)
        if new_block:
            self.add_block_widget(new_block)
    
    def add_block_widget(self, block: DocumentBlockEntity):
        """افزودن ویجت بلوک به لیست"""
        block_widget = BlockWidget(block, self)
        block_widget.block_changed.connect(self.on_block_changed)
        block_widget.block_deleted.connect(self.on_block_deleted)
        block_widget.block_moved.connect(self.on_block_moved)
        
        self.blocks_widgets[block.id] = block_widget
        
        # افزودن به layout (قبل از stretch)
        count = self.blocks_layout.count()
        self.blocks_layout.insertWidget(count - 1, block_widget)
    
    def on_block_changed(self, block_id: str, block_type: str, content: str):
        """وقتی بلوک تغییر می‌کند"""
        block = self.blocks_widgets.get(block_id)
        if block:
            block_metadata = block.block.block_metadata if hasattr(block.block, 'block_metadata') else None
            self.service.update_block(block_id, block_type, content, None, block_metadata)
    
    def on_block_deleted(self, block_id: str):
        """حذف بلوک"""
        reply = QMessageBox.question(
            self, "حذف بلوک", "آیا مطمئن هستید که می‌خواهید این بلوک را حذف کنید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.service.delete_block(block_id)
            widget = self.blocks_widgets.pop(block_id, None)
            if widget:
                widget.deleteLater()
    
    def on_block_moved(self, block_id: str, direction: int):
        """جابه‌جایی بلوک"""
        # دریافت بلوک‌ها از دیتابیس با ترتیب فعلی
        blocks = self.service.get_document_blocks(self.document_id)
        block_ids = [b.id for b in blocks]
        
        try:
            current_index = block_ids.index(block_id)
            new_index = current_index + direction
            
            if 0 <= new_index < len(block_ids):
                # جابه‌جایی در لیست
                block_ids[current_index], block_ids[new_index] = block_ids[new_index], block_ids[current_index]
                
                # به‌روزرسانی ترتیب در دیتابیس
                block_orders = {bid: idx for idx, bid in enumerate(block_ids)}
                self.service.reorder_blocks(self.document_id, block_orders)
                
                # جابه‌جایی ویجت‌ها در layout
                self.reorder_blocks_layout(block_ids)
        except (ValueError, IndexError):
            pass
    
    def reorder_blocks_layout(self, block_ids: list):
        """تغییر ترتیب ویجت‌ها در layout بدون حذف"""
        # حذف همه ویجت‌ها از layout (بدون حذف خود ویجت‌ها)
        widgets_to_reorder = []
        while self.blocks_layout.count() > 1:  # نگه داشتن stretch
            item = self.blocks_layout.takeAt(0)
            if item.widget():
                widgets_to_reorder.append(item.widget())
        
        # افزودن مجدد با ترتیب جدید
        for block_id in block_ids:
            if block_id in self.blocks_widgets:
                widget = self.blocks_widgets[block_id]
                if widget in widgets_to_reorder:
                    self.blocks_layout.insertWidget(
                        self.blocks_layout.count() - 1,
                        widget
                    )
    
    def save_document(self):
        """ذخیره سند"""
        try:
            title = self.title_input.text() or "سند جدید"
            course_id = self.course_combo.currentData()
            textbook_id = self.textbook_combo.currentData()
            
            if self.document_id:
                self.service.update_document(self.document_id, title, course_id, textbook_id)
            else:
                self.document_id = self.service.create_document(title, course_id, textbook_id)
            
            # ذخیره همه بلوک‌ها
            for block_id, widget in self.blocks_widgets.items():
                content = widget.get_content()
                block_metadata = widget.block.block_metadata if hasattr(widget.block, 'block_metadata') else None
                self.service.update_block(block_id, widget.block.block_type, content, None, block_metadata)
            
            QMessageBox.information(self, "موفق", "سند با موفقیت ذخیره شد.")
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ذخیره سند: {str(e)}")
    
    def apply_theme(self):
        from utils.app_config import AppConfig
        is_dark = AppConfig.get_theme() == "دارک"
        
        if is_dark:
            style = """
                QWidget { background-color: #1e1e1e; color: white; }
                QLineEdit, QTextEdit, QComboBox {
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
                QLineEdit, QTextEdit, QComboBox {
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

