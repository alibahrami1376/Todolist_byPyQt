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
    QMessageBox,
    QGraphicsDropShadowEffect,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QTextDocument

from services.project_service import ProjectService


class ProjectsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = ProjectService()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        header = QHBoxLayout()
        title = QLabel("Projects")
        title.setStyleSheet("font-size: 22px; font-weight: 600; letter-spacing: 0.4px;")
        header.addWidget(title)
        header.addStretch()
        add_btn = QPushButton("New Project")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setFixedHeight(38)
        add_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3b82f6;
                color: #f9fafb;
                border-radius: 12px;
                padding: 8px 18px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #4b8dfa;
            }
            QPushButton:pressed {
                background-color: #2b6fdc;
            }
        """
        )
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
            QListWidget::item:selected {
                background-color: rgba(59, 130, 246, 0.08);
                border-radius: 12px;
            }
        """
        )
        layout.addWidget(self.list_widget)

        self.load_projects()

    def load_projects(self):
        self.list_widget.clear()
        projects = self.service.list_all()
        content_width = max(self.list_widget.viewport().width() - 120, 320)
        for pid, title, desc, status, created in projects:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, pid)
            card = self._build_project_card(pid, title, desc, status, created, content_width)
            item.setSizeHint(card.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, card)

    def _build_project_card(self, project_id: str, title: str, description: str, status: str, created_at: str, content_width: int) -> QWidget:
        card = QFrame()
        card.setObjectName("projectCard")
        card.setStyleSheet(
            """
            QFrame#projectCard {
                background-color: #1f2430;
                border: 1px solid #2f333d;
                border-radius: 16px;
            }
        """
        )
        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 12)
        shadow.setColor(QColor(0, 0, 0, 80))
        card.setGraphicsEffect(shadow)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(8)

        header = QHBoxLayout()
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 600; color: #f3f4f6;")
        header.addWidget(title_lbl)
        header.addStretch()
        status_badge = QLabel(self._status_text(status))
        badge_bg, badge_color = self._status_palette(status)
        status_badge.setStyleSheet(
            f"padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; background-color: {badge_bg}; color: {badge_color};"
        )
        header.addWidget(status_badge)
        delete_btn = QPushButton("Delete")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setStyleSheet(
            """
            QPushButton {
                min-width: 72px;
                padding: 4px 10px;
                border-radius: 10px;
                background-color: rgba(244, 63, 94, 0.12);
                color: #f43f5e;
                border: 1px solid rgba(244, 63, 94, 0.3);
            }
            QPushButton:hover {
                background-color: rgba(244, 63, 94, 0.2);
            }
        """
        )
        delete_btn.clicked.connect(lambda _, pid=project_id: self.delete_project(pid))
        header.addWidget(delete_btn)
        layout.addLayout(header)

        desc_frame = QFrame()
        desc_frame.setStyleSheet(
            """
            QFrame {
                background-color: rgba(255, 255, 255, 0.02);
                border: 1px dashed #2c313d;
                border-radius: 12px;
            }
        """
        )
        desc_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        desc_layout = QVBoxLayout(desc_frame)
        desc_layout.setContentsMargins(12, 8, 12, 10)
        safe_description = description or "No description provided"
        desc_lbl = QLabel(safe_description)
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("color: #c5cad8; line-height: 1.4;")
        desc_lbl.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        desc_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        desc_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        text_height = self._measure_text_height(safe_description, content_width - 64)
        desc_lbl.setMinimumHeight(text_height)
        desc_layout.addWidget(desc_lbl)
        layout.addWidget(desc_frame)

        footer = QHBoxLayout()
        footer.setSpacing(12)
        meta = QLabel(f"Created: {created_at}")
        meta.setStyleSheet("color: #7f848e; font-size: 12px; letter-spacing: 0.3px;")
        footer.addWidget(meta)
        footer.addStretch()
        steps_btn = QPushButton("Steps")
        steps_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        steps_btn.setStyleSheet(
            """
            QPushButton {
                padding: 5px 14px;
                border-radius: 10px;
                border: 1px solid rgba(139, 92, 246, 0.5);
                color: #c4b5fd;
                background-color: transparent;
            }
            QPushButton:hover {
                border-color: rgba(196, 181, 253, 0.85);
                color: #e0d4ff;
            }
        """
        )
        steps_btn.clicked.connect(lambda _, pid=project_id: self.open_steps_dialog(pid))
        footer.addWidget(steps_btn)

        detail_btn = QPushButton("Details")
        detail_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        detail_btn.setStyleSheet(
            """
            QPushButton {
                padding: 5px 14px;
                border-radius: 10px;
                border: 1px solid rgba(86, 156, 214, 0.5);
                color: #8ab4f8;
                background-color: transparent;
            }
            QPushButton:hover {
                border-color: rgba(138, 180, 248, 0.8);
                color: #b3d4ff;
            }
        """
        )
        detail_btn.clicked.connect(lambda _, pid=project_id: self.open_detail_dialog(pid))
        footer.addWidget(detail_btn)
        layout.addLayout(footer)

        return card

    def _status_text(self, status: str) -> str:
        mapping = {
            "todo": "Backlog",
            "doing": "In Progress",
            "done": "Complete",
        }
        return mapping.get(status, status or "Unknown")

    def _status_palette(self, status: str) -> tuple[str, str]:
        mapping = {
            "todo": ("rgba(250, 204, 21, 0.18)", "#facc15"),
            "doing": ("rgba(59, 130, 246, 0.18)", "#60a5fa"),
            "done": ("rgba(16, 185, 129, 0.18)", "#34d399"),
        }
        return mapping.get(status, ("rgba(86, 156, 214, 0.15)", "#8ab4f8"))

    def _measure_text_height(self, text: str, width: int) -> int:
        doc = QTextDocument()
        doc.setDefaultFont(self.font())
        doc.setPlainText(text or "")
        doc.setTextWidth(max(width, 220))
        # add a bit of padding so the last line never clips
        return int(doc.size().height() + 6)

    def delete_project(self, project_id: str):
        confirm = QMessageBox.question(
            self,
            "Delete Project",
            "Deleting this project removes every related step. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        self.service.delete(project_id)
        self.load_projects()

    def on_project_clicked(self, item: QListWidgetItem):
        project_id = item.data(Qt.ItemDataRole.UserRole)
        if not project_id:
            return

        self.open_detail_dialog(project_id)

    def open_detail_dialog(self, project_id: str):
        if not project_id:
            return
        from views.pages.project_detail_page import ProjectDetailPage

        detail_dialog = ProjectDetailPage(project_id)
        detail_dialog.exec()

    def open_steps_dialog(self, project_id: str):
        if not project_id:
            return
        from views.pages.project_steps_page import ProjectStepsDialog

        steps_dialog = ProjectStepsDialog(project_id)
        steps_dialog.exec()

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
        self.setWindowTitle("Create Project")
        self.setMinimumWidth(420)
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.addWidget(QLabel("Title"))
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Project title...")
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("Summary"))
        self.summary_edit = QTextEdit()
        self.summary_edit.setPlaceholderText("Describe the goal or outcome")
        self.summary_edit.setMinimumHeight(100)
        layout.addWidget(self.summary_edit)
        layout.addWidget(QLabel("Idea ID (optional)"))
        self.idea_edit = QLineEdit()
        self.idea_edit.setPlaceholderText("Link an existing idea if needed")
        layout.addWidget(self.idea_edit)
        btns = QHBoxLayout()
        btns.addStretch()
        ok = QPushButton("Save")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("Cancel")
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


