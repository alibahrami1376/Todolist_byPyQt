from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from services.project_service import ProjectService
from services.learning_path_service import LearningPathService
from utils.app_notifier import AppNotifier


class IdeaWorkspacePage(QDialog):
    def __init__(self, idea_id: str, idea_title: str, idea_summary: str = "", idea_goal: str = "", idea_created_at: str = ""):
        super().__init__()
        self.setWindowTitle(f"Workspace: {idea_title}")
        self.idea_id = idea_id
        self.project_service = ProjectService()
        self.learning_service = LearningPathService()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        header = QLabel(f"پروژه‌ها و مسیرهای یادگیری برای: {idea_title}")
        layout.addWidget(header)
        # نمایش جزئیات ایده را مینیمال نگه می‌داریم تا تمرکز روی آیکن‌ها باشد

        # Projects section
        proj_header = QHBoxLayout()
        proj_header.addWidget(QLabel("پروژه‌ها"))
        proj_header.addStretch()
        btn_add_proj = QPushButton("ایجاد پروژه")
        btn_add_proj.clicked.connect(self.open_create_project)
        proj_header.addWidget(btn_add_proj)
        layout.addLayout(proj_header)

        self.projects_list = QListWidget()
        self.projects_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.projects_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.projects_list.setIconSize(QSize(72, 72))
        self.projects_list.setGridSize(QSize(140, 140))
        self.projects_list.setSpacing(12)
        layout.addWidget(self.projects_list)

        # Learning paths section
        lp_header = QHBoxLayout()
        lp_header.addWidget(QLabel("مسیرهای یادگیری"))
        lp_header.addStretch()
        btn_add_lp = QPushButton("ایجاد مسیر")
        btn_add_lp.clicked.connect(self.open_create_learning_path)
        lp_header.addWidget(btn_add_lp)
        layout.addLayout(lp_header)

        self.learning_list = QListWidget()
        self.learning_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.learning_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.learning_list.setIconSize(QSize(64, 64))
        self.learning_list.setGridSize(QSize(140, 140))
        self.learning_list.setSpacing(12)
        layout.addWidget(self.learning_list)

        self.load_projects()

    def load_projects(self):
        self.projects_list.clear()
        icon = QIcon("icons/project.png") if QIcon("icons/project.png").availableSizes() else QIcon("icons/information.png")
        for pid, title, desc, status, created in self.project_service.list_by_idea(self.idea_id):
            item = QListWidgetItem(icon, title)
            item.setData(Qt.ItemDataRole.UserRole, pid)
            self.projects_list.addItem(item)
        # پس از بارگذاری پروژه‌ها، همه مسیرهای مربوطه را نیز نمایش بده
        self.load_learning_paths()

    def load_learning_paths(self):
        self.learning_list.clear()
        icon = QIcon("icons/learning.png") if QIcon("icons/learning.png").availableSizes() else QIcon("icons/information.png")
        for i in range(self.projects_list.count()):
            pid_item = self.projects_list.item(i)
            pid = pid_item.data(Qt.ItemDataRole.UserRole)
            for lid, title, content, order_index, created in self.learning_service.list_by_project(pid):
                item = QListWidgetItem(icon, title)
                item.setData(Qt.ItemDataRole.UserRole, lid)
                self.learning_list.addItem(item)

    def open_create_project(self):
        dlg = ProjectCreateDialog()
        if dlg.exec():
            title, description = dlg.get_values()
            if not title:
                AppNotifier(QDialog).warning("خطا", "عنوان پروژه الزامی است")
            else:
                self.project_service.add(self.idea_id, title=title, description=description)
                self.load_projects()

    def open_create_learning_path(self):
        if self.projects_list.count() == 0:
            AppNotifier(QDialog).warning("هشدار", "ابتدا یک پروژه ایجاد کنید")
            return
        dlg = LearningPathCreateDialog()
        if dlg.exec():
            title, content = dlg.get_values()
            if not title:
                AppNotifier(QDialog).warning("خطا", "عنوان مسیر الزامی است")
            else:
                # اضافه کردن به اولین پروژه؛ در آینده می‌توان انتخاب پروژه را افزود
                first_pid = self.projects_list.item(0).data(Qt.ItemDataRole.UserRole)
                order_index = self.learning_list.count()
                self.learning_service.add(first_pid, title=title, content=content, order_index=order_index)
                self.load_learning_paths()


class ProjectCreateDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ایجاد پروژه")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("عنوان"))
        self.title_edit = QLineEdit()
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("توضیحات"))
        self.desc_edit = QTextEdit()
        layout.addWidget(self.desc_edit)
        btns = QHBoxLayout()
        ok = QPushButton("ذخیره")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("انصراف")
        cancel.clicked.connect(self.reject)
        btns.addWidget(ok)
        btns.addWidget(cancel)
        layout.addLayout(btns)

    def get_values(self):
        return self.title_edit.text().strip(), self.desc_edit.toPlainText().strip()


class LearningPathCreateDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ایجاد مسیر یادگیری")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("عنوان"))
        self.title_edit = QLineEdit()
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("توضیحات/محتوا"))
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
        return self.title_edit.text().strip(), self.content_edit.toPlainText().strip()


