from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QPushButton, QDialog, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from services.learning_path_service import LearningPathService


class LearningPathsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = LearningPathService()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QHBoxLayout()
        header.addWidget(QLabel("مسیرهای یادگیری"))
        header.addStretch()
        add_btn = QPushButton("ایجاد مسیر")
        add_btn.clicked.connect(self.open_create)
        header.addWidget(add_btn)
        layout.addLayout(header)

        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setIconSize(QSize(64, 64))
        self.list_widget.setGridSize(QSize(140, 140))
        self.list_widget.setSpacing(12)
        layout.addWidget(self.list_widget)

        self.load_paths_for_none()

    def load_paths_for_none(self):
        self.list_widget.clear()
        # leaving empty by design; could be extended to list recent paths across projects

    def open_create(self):
        dlg = LearningPathGlobalDialog()
        if dlg.exec():
            project_id, title, content = dlg.get_values()
            if project_id and title:
                self.service.add(project_id, title=title, content=content, order_index=0)
                self.load_paths_for_none()


class LearningPathGlobalDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ایجاد مسیر یادگیری")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Project ID"))
        self.project_edit = QLineEdit()
        layout.addWidget(self.project_edit)
        layout.addWidget(QLabel("عنوان"))
        self.title_edit = QLineEdit()
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("محتوا"))
        self.content_edit = QTextEdit()
        layout.addWidget(self.content_edit)
        btns = QHBoxLayout()
        ok = QPushButton("ذخیره")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("انصراف")
        cancel.clicked.connect(self.reject)
        btns.addWidget(ok)
        btns.addWidget(cancel)
        layout.addLayout(btns)

    def get_values(self):
        return (
            self.project_edit.text().strip(),
            self.title_edit.text().strip(),
            self.content_edit.toPlainText().strip(),
        )


