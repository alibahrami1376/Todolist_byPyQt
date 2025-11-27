from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QPushButton,
    QDialog,
    QLineEdit,
    QTextEdit,
    QFrame,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from services.project_service import ProjectService


class ProjectsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = ProjectService()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        header = QHBoxLayout()
        title = QLabel("پروژه‌ها")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()
        add_btn = QPushButton("ایجاد پروژه")
        add_btn.clicked.connect(self.open_create)
        header.addWidget(add_btn)
        layout.addLayout(header)

        self.list_widget = QListWidget()
        self.list_widget.setSpacing(16)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setViewMode(QListWidget.ViewMode.ListMode)
        self.list_widget.setMovement(QListWidget.Movement.Static)
        self.list_widget.setUniformItemSizes(False)
        self.list_widget.itemDoubleClicked.connect(self.on_project_clicked)
        self.list_widget.setStyleSheet(
            """
            QListWidget {
                background-color: transparent;
                border: none;
            }
        """
        )
        layout.addWidget(self.list_widget)

        self.load_projects()

    def load_projects(self):
        self.list_widget.clear()
        projects = self.service.list_all()
        for pid, title, desc, status, created in projects:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, pid)
            card = self._build_project_card(title, desc, status, created)
            item.setSizeHint(card.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, card)

    def _build_project_card(self, title: str, description: str, status: str, created_at: str) -> QWidget:
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #1f2430;
                border: 1px solid #2f333d;
                border-radius: 16px;
            }
        """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(8)

        header = QHBoxLayout()
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 600; color: #f3f4f6;")
        header.addWidget(title_lbl)
        header.addStretch()
        status_badge = QLabel(self._status_text(status))
        status_badge.setStyleSheet(
            "padding: 4px 10px; border-radius: 12px; background-color: rgba(86,156,214,0.18); color: #569cd6; font-size: 12px;"
        )
        header.addWidget(status_badge)
        layout.addLayout(header)

        desc_lbl = QLabel(description or "بدون توضیحات")
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("color: #b0b6c3;")
        layout.addWidget(desc_lbl)

        meta = QLabel(f"ایجاد: {created_at}")
        meta.setStyleSheet("color: #7f848e; font-size: 12px;")
        layout.addWidget(meta)

        return card

    def _status_text(self, status: str) -> str:
        mapping = {
            "todo": "در انتظار",
            "doing": "در حال انجام",
            "done": "تکمیل شده",
        }
        return mapping.get(status, status or "نامشخص")

    def on_project_clicked(self, item: QListWidgetItem):
        project_id = item.data(Qt.ItemDataRole.UserRole)
        if not project_id:
            return

        from views.pages.project_detail_page import ProjectDetailPage
        detail_dialog = ProjectDetailPage(project_id)
        detail_dialog.exec()

    def open_create(self):
        dlg = ProjectCreateGlobalDialog()
        if dlg.exec():
            title, summary, idea_id = dlg.get_values()
            if title and idea_id:
                self.service.add(idea_id=idea_id, title=title, description=summary)
                self.load_projects()


class ProjectCreateGlobalDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ایجاد پروژه جدید")
        self.setMinimumWidth(420)
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.addWidget(QLabel("عنوان"))
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("عنوان پروژه...")
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("خلاصه"))
        self.summary_edit = QTextEdit()
        self.summary_edit.setPlaceholderText("چند خط درباره هدف یا خروجی پروژه بنویسید")
        self.summary_edit.setMinimumHeight(100)
        layout.addWidget(self.summary_edit)
        layout.addWidget(QLabel("شناسه ایده (اختیاری)"))
        self.idea_edit = QLineEdit()
        self.idea_edit.setPlaceholderText("در صورت نیاز، شناسه ایده مرتبط را وارد کنید")
        layout.addWidget(self.idea_edit)
        btns = QHBoxLayout()
        btns.addStretch()
        ok = QPushButton("ذخیره")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("انصراف")
        cancel.clicked.connect(self.reject)
        btns.addWidget(cancel)
        btns.addWidget(ok)
        layout.addLayout(btns)

    def get_values(self):
        return (
            self.title_edit.text().strip(),
            self.summary_edit.toPlainText().strip(),
            self.idea_edit.text().strip(),
        )


