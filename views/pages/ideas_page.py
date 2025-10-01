from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QDialog, QTextEdit
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
import uuid

from services.idea_service import IdeaService
from utils.app_notifier import AppNotifier


class IdeaDetailDialog(QDialog):
    def __init__(self, idea_id: str, title: str, description: str, created_at: str, service: IdeaService):
        super().__init__()
        self.setWindowTitle("جزئیات ایده")
        self.idea_id = idea_id
        self.service = service
        self.deleted = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        layout.addWidget(QLabel(f"عنوان: {title}"))
        desc = QTextEdit()
        desc.setReadOnly(True)
        desc.setPlainText(description or "")
        layout.addWidget(desc)
        layout.addWidget(QLabel(f"تاریخ ایجاد: {created_at}"))

        btns = QHBoxLayout()
        btn_delete = QPushButton("حذف")
        btn_delete.clicked.connect(self._delete)
        btns.addWidget(btn_delete)

        btn_close = QPushButton("بستن")
        btn_close.clicked.connect(self.accept)
        btns.addWidget(btn_close)
        layout.addLayout(btns)

    def _delete(self):
        if AppNotifier(QWidget).confirm("حذف", "آیا از حذف این ایده مطمئن هستید؟"):
            self.service.delete_idea(self.idea_id)
            self.deleted = True
            self.accept()


class IdeaEditorDialog(QDialog):
    def __init__(self, service: IdeaService):
        super().__init__()
        self.setWindowTitle("ایده جدید")
        self.service = service
        self.saved = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.input_title = QLabel("عنوان ایده")
        layout.addWidget(self.input_title)
        from PyQt6.QtWidgets import QLineEdit
        self.title_line = QLineEdit()
        layout.addWidget(self.title_line)

        layout.addWidget(QLabel("توضیحات"))
        self.desc_edit = QTextEdit()
        layout.addWidget(self.desc_edit)

        btns = QHBoxLayout()
        btn_save = QPushButton("ذخیره")
        btn_save.clicked.connect(self._save)
        btns.addWidget(btn_save)
        btn_cancel = QPushButton("انصراف")
        btn_cancel.clicked.connect(self.reject)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

    def _save(self):
        title = self.title_line.text().strip()
        description = self.desc_edit.toPlainText().strip()
        if not title:
            AppNotifier(QWidget).warning("خطا", "عنوان ایده الزامی است")
            return
        self.service.add_idea(uuid.uuid4().hex, title, description)
        self.saved = True
        self.accept()


class IdeasPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = IdeaService()
        self.init_ui()
        self.load_ideas()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QHBoxLayout()
        title = QLabel("ایده‌ها")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header.addWidget(title)
        header.addStretch()
        add_btn = QPushButton("ایده جدید")
        add_btn.clicked.connect(self.new_idea)
        header.addWidget(add_btn)
        layout.addLayout(header)

        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setIconSize(QSize(96, 96))
        self.list_widget.setGridSize(QSize(140, 140))
        self.list_widget.setSpacing(12)
        self.list_widget.itemClicked.connect(self.open_detail)
        layout.addWidget(self.list_widget)

    def load_ideas(self):
        self.list_widget.clear()
        icon = QIcon("icons/information.png")
        for id_value, title, description, created_at in self.service.list_ideas():
            item = QListWidgetItem(icon, title)
            item.setData(Qt.ItemDataRole.UserRole, (id_value, title, description, created_at))
            item.setSizeHint(QSize(120, 120))
            self.list_widget.addItem(item)

    def open_detail(self, item: QListWidgetItem):
        id_value, title, description, created_at = item.data(Qt.ItemDataRole.UserRole)
        dlg = IdeaDetailDialog(id_value, title, description, created_at, self.service)
        dlg.exec()
        if dlg.deleted:
            self.load_ideas()

    def new_idea(self):
        dlg = IdeaEditorDialog(self.service)
        dlg.exec()
        if dlg.saved:
            self.load_ideas()


