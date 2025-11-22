from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QDialog, QTextEdit
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
import uuid

from services.idea_service import IdeaService
from utils.app_notifier import AppNotifier
from views.pages.idea_workspace_page import IdeaWorkspacePage


class IdeaDetailDialog(QDialog):
    def __init__(self, idea_id: str, title: str, summary: str, goal: str, created_at: str, service: IdeaService):
        super().__init__()
        self.setWindowTitle("جزئیات ایده")
        self.idea_id = idea_id
        self.service = service
        self.deleted = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        layout.addWidget(QLabel(f"عنوان: {title}"))
        layout.addWidget(QLabel("خلاصه"))
        summary_view = QTextEdit()
        summary_view.setReadOnly(True)
        summary_view.setPlainText(summary or "")
        layout.addWidget(summary_view)
        layout.addWidget(QLabel("هدف"))
        goal_view = QTextEdit()
        goal_view.setReadOnly(True)
        goal_view.setPlainText(goal or "")
        layout.addWidget(goal_view)
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
        self.setMinimumSize(500, 600)
        self.service = service
        self.saved = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        from PyQt6.QtWidgets import QLineEdit, QComboBox, QSpinBox
        from PyQt6.QtCore import QSize
        
        layout.addWidget(QLabel("عنوان ایده *"))
        self.title_line = QLineEdit()
        layout.addWidget(self.title_line)

        layout.addWidget(QLabel("توضیحات"))
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        layout.addWidget(self.description_edit)

        layout.addWidget(QLabel("دسته‌بندی"))
        self.category_edit = QLineEdit()
        layout.addWidget(self.category_edit)

        layout.addWidget(QLabel("تگ‌ها (با کاما جدا کنید)"))
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("مثال: python, web, api")
        layout.addWidget(self.tags_edit)

        layout.addWidget(QLabel("اولویت"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["low", "medium", "high"])
        self.priority_combo.setCurrentText("medium")
        layout.addWidget(self.priority_combo)

        layout.addWidget(QLabel("امتیاز (0-100)"))
        self.score_spin = QSpinBox()
        self.score_spin.setRange(0, 100)
        self.score_spin.setValue(0)
        layout.addWidget(self.score_spin)

        # Keep old fields for backward compatibility
        layout.addWidget(QLabel("خلاصه (اختیاری)"))
        self.summary_edit = QTextEdit()
        self.summary_edit.setMaximumHeight(80)
        layout.addWidget(self.summary_edit)

        layout.addWidget(QLabel("هدف (اختیاری)"))
        self.goal_edit = QTextEdit()
        self.goal_edit.setMaximumHeight(80)
        layout.addWidget(self.goal_edit)

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
        description = self.description_edit.toPlainText().strip()
        category = self.category_edit.text().strip()
        tags = self.tags_edit.text().strip()
        priority = self.priority_combo.currentText()
        score = self.score_spin.value()
        summary = self.summary_edit.toPlainText().strip()
        goal = self.goal_edit.toPlainText().strip()
        
        if not title:
            AppNotifier(QWidget).warning("خطا", "عنوان ایده الزامی است")
            return
        
        idea_id = uuid.uuid4().hex
        self.service.add_idea(
            idea_id, 
            title, 
            summary, 
            goal,
            description=description,
            category=category,
            tags=tags,
            priority=priority,
            score=score
        )
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
        for id_value, title, summary, created_at in self.service.list_ideas():
            item = QListWidgetItem(icon, title)
            item.setData(Qt.ItemDataRole.UserRole, (id_value, title, summary, created_at))
            item.setSizeHint(QSize(120, 120))
            self.list_widget.addItem(item)

    def open_detail(self, item: QListWidgetItem):
        id_value, title, summary, created_at = item.data(Qt.ItemDataRole.UserRole)
        _id, _title, summary_full, goal_full, created_at_full = self.service.get_idea(id_value)
        workspace = IdeaWorkspacePage(idea_id=id_value, idea_title=title, idea_summary=summary_full, idea_goal=goal_full, idea_created_at=created_at_full)
        workspace.exec()
        self.load_ideas()

    def new_idea(self):
        dlg = IdeaEditorDialog(self.service)
        dlg.exec()
        if dlg.saved:
            self.load_ideas()


