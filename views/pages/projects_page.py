from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QPushButton, QDialog, QLineEdit, QTextEdit, QComboBox
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from services.project_service import ProjectService


class ProjectsPage(QWidget):
    def load_projects(self):
        self.list_widget.clear()
        icon = QIcon("icons/project.png") if QIcon("icons/project.png").availableSizes() else QIcon("icons/information.png")
        projects = self.service.list_all()
        for pid, title, desc, status, created in projects:
            item = QListWidgetItem(icon, title)
            item.setData(Qt.ItemDataRole.UserRole, pid)
            self.list_widget.addItem(item)
    def open_create(self):
        dlg = ProjectCreateGlobalDialog()
        if dlg.exec():
            (
                title,
                summary,
                start_time,
                end_time,
                required_hours,
                status,
                priority,
                idea_id,
            ) = dlg.get_values()
            if title and idea_id:
                # اگر متد add سرویس پروژه فقط title و description می‌گیرد، باید آن را توسعه دهید
                self.service.add(
                    idea_id=idea_id,
                    title=title,
                    description=summary,
                    start_time=start_time,
                    end_time=end_time,
                    required_hours=required_hours,
                    status=status,
                    priority=priority,
                )
                self.load_projects()


    def __init__(self):

        super().__init__()
        self.service = ProjectService()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QHBoxLayout()
        header.addWidget(QLabel("پروژه‌ها"))
        header.addStretch()
        add_btn = QPushButton("ایجاد پروژه")
        add_btn.clicked.connect(self.open_create)
        header.addWidget(add_btn)
        layout.addLayout(header)

        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.ViewMode.IconMode)
        self.list_widget.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.list_widget.setIconSize(QSize(72, 72))
        self.list_widget.setGridSize(QSize(140, 140))
        self.list_widget.setSpacing(12)
        layout.addWidget(self.list_widget)

        self.load_projects()
        self.list_widget.itemClicked.connect(self.show_project_details)

     


    def show_project_details(self, item):
        pid = item.data(Qt.ItemDataRole.UserRole)
        project = self.service.get_by_id(pid) if hasattr(self.service, 'get_by_id') else None
        if project:
            dlg = ProjectDetailsDialog(project)
            dlg.exec()
        else:
            # اگر متد get_by_id وجود ندارد یا پروژه پیدا نشد
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "جزئیات پروژه", "اطلاعات پروژه یافت نشد.")


class ProjectDetailsDialog(QDialog):

    def __init__(self, project):
        super().__init__()
        self.setWindowTitle("جزئیات پروژه")
        layout = QVBoxLayout(self)
        # فرض بر این است که project یک دیکشنری یا tuple است
        # اگر دیکشنری بود:
        if isinstance(project, dict):
            layout.addWidget(QLabel(f"عنوان: {project.get('title', '')}"))
            layout.addWidget(QLabel(f"خلاصه: {project.get('description', '')}"))
            layout.addWidget(QLabel(f"شروع ساعت: {project.get('start_time', '')}"))
            layout.addWidget(QLabel(f"پایان ساعت: {project.get('end_time', '')}"))
            layout.addWidget(QLabel(f"ساعت مورد نیاز: {project.get('required_hours', '')}"))
            layout.addWidget(QLabel(f"وضعیت: {project.get('status', '')}"))
            layout.addWidget(QLabel(f"اهمیت: {project.get('priority', '')}"))
            layout.addWidget(QLabel(f"Idea ID: {project.get('idea_id', '')}"))
        else:
            # اگر tuple بود، به ترتیب نمایش بده
            for label, value in zip([
                "عنوان", "خلاصه", "شروع ساعت", "پایان ساعت", "ساعت مورد نیاز", "وضعیت", "اهمیت", "Idea ID"], project):
                layout.addWidget(QLabel(f"{label}: {value}"))
        btns = QHBoxLayout()
        close_btn = QPushButton("بستن")
        close_btn.clicked.connect(self.accept)
        btns.addWidget(close_btn)
        layout.addLayout(btns)

    def load_projects(self):
        self.list_widget.clear()
        icon = QIcon("icons/project.png") if QIcon("icons/project.png").availableSizes() else QIcon("icons/information.png")
        projects = self.service.list_all()
        for pid, title, desc, status, created in projects:
            item = QListWidgetItem(icon, title)
            item.setData(Qt.ItemDataRole.UserRole, pid)
            self.list_widget.addItem(item)

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
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("عنوان"))
        self.title_edit = QLineEdit()
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("خلاصه"))
        self.summary_edit = QTextEdit()
        layout.addWidget(self.summary_edit)

        # شروع ساعت
        layout.addWidget(QLabel("شروع ساعت"))
        self.start_time_edit = QLineEdit()
        self.start_time_edit.setPlaceholderText("مثال: 08:00")
        layout.addWidget(self.start_time_edit)

        # پایان ساعت
        layout.addWidget(QLabel("پایان ساعت"))
        self.end_time_edit = QLineEdit()
        self.end_time_edit.setPlaceholderText("مثال: 17:00")
        layout.addWidget(self.end_time_edit)

        # ساعت مورد نیاز پروژه
        layout.addWidget(QLabel("ساعت مورد نیاز پروژه"))
        self.required_hours_edit = QLineEdit()
        self.required_hours_edit.setPlaceholderText("مثال: 40")
        layout.addWidget(self.required_hours_edit)

        # وضعیت انجام
        layout.addWidget(QLabel("وضعیت انجام"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["در حال انجام", "تکمیل شده", "متوقف شده"])
        layout.addWidget(self.status_combo)

        # اهمیت
        layout.addWidget(QLabel("اهمیت"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["کم", "متوسط", "زیاد"])
        layout.addWidget(self.priority_combo)

        layout.addWidget(QLabel("Idea ID"))
        self.idea_edit = QLineEdit()
        layout.addWidget(self.idea_edit)
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
            self.title_edit.text().strip(),
            self.summary_edit.toPlainText().strip(),
            self.start_time_edit.text().strip(),
            self.end_time_edit.text().strip(),
            self.required_hours_edit.text().strip(),
            self.status_combo.currentText(),
            self.priority_combo.currentText(),
            self.idea_edit.text().strip(),
        )


