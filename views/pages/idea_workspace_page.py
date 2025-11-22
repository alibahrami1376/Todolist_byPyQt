from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, 
    QListWidgetItem, QLineEdit, QTextEdit, QComboBox, QSpinBox, QDateEdit, QTabWidget, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QSize, QDate
from PyQt6.QtGui import QIcon

from services.project_service import ProjectService
from services.project_step_service import ProjectStepService
from services.learning_path_service import LearningPathService
from utils.app_notifier import AppNotifier


class IdeaWorkspacePage(QDialog):
    def __init__(self, idea_id: str, idea_title: str, idea_summary: str = "", idea_goal: str = "", idea_created_at: str = ""):
        super().__init__()
        self.setWindowTitle(f"Workspace: {idea_title}")
        self.idea_id = idea_id
        self.project_service = ProjectService()
        self.step_service = ProjectStepService()
        self.learning_service = LearningPathService()
        self.current_project_id = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        header = QLabel(f"<h2>پروژه‌ها و مراحل برای: {idea_title}</h2>")
        layout.addWidget(header)

        # Create tabs for Projects and Steps
        self.tabs = QTabWidget()
        
        # Projects tab
        projects_tab = QWidget()
        projects_layout = QVBoxLayout(projects_tab)
        
        proj_header = QHBoxLayout()
        proj_header.addWidget(QLabel("<b>پروژه‌ها</b>"))
        proj_header.addStretch()
        btn_add_proj = QPushButton("ایجاد پروژه")
        btn_add_proj.clicked.connect(self.open_create_project)
        proj_header.addWidget(btn_add_proj)
        projects_layout.addLayout(proj_header)

        self.projects_list = QListWidget()
        self.projects_list.setViewMode(QListWidget.ViewMode.ListMode)
        self.projects_list.itemClicked.connect(self.on_project_selected)
        projects_layout.addWidget(self.projects_list)
        
        self.tabs.addTab(projects_tab, "پروژه‌ها")

        # Project Steps tab
        steps_tab = QWidget()
        steps_layout = QVBoxLayout(steps_tab)
        
        steps_header = QHBoxLayout()
        steps_header.addWidget(QLabel("<b>مراحل پروژه</b>"))
        steps_header.addStretch()
        self.btn_add_step = QPushButton("افزودن مرحله")
        self.btn_add_step.clicked.connect(self.open_create_step)
        self.btn_add_step.setEnabled(False)
        steps_header.addWidget(self.btn_add_step)
        steps_layout.addLayout(steps_header)

        self.steps_table = QTableWidget()
        self.steps_table.setColumnCount(5)
        self.steps_table.setHorizontalHeaderLabels(["عنوان", "توضیحات", "وضعیت", "ترتیب", "عملیات"])
        self.steps_table.horizontalHeader().setStretchLastSection(True)
        self.steps_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        steps_layout.addWidget(self.steps_table)
        
        self.tabs.addTab(steps_tab, "مراحل پروژه")

        layout.addWidget(self.tabs)
        self.load_projects()

    def load_projects(self):
        self.projects_list.clear()
        for pid, title, desc, status, created, progress, _ in self.project_service.list_by_idea(self.idea_id):
            item_text = f"{title} | وضعیت: {status} | پیشرفت: {progress}%"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, pid)
            self.projects_list.addItem(item)
    
    def on_project_selected(self, item: QListWidgetItem):
        self.current_project_id = item.data(Qt.ItemDataRole.UserRole)
        self.btn_add_step.setEnabled(True)
        self.load_steps()
        self.tabs.setCurrentIndex(1)  # Switch to steps tab
    
    def load_steps(self):
        if not self.current_project_id:
            return
        steps = self.step_service.list_by_project(self.current_project_id)
        self.steps_table.setRowCount(len(steps))
        for row, (step_id, title, description, status, order) in enumerate(steps):
            self.steps_table.setItem(row, 0, QTableWidgetItem(title))
            self.steps_table.setItem(row, 1, QTableWidgetItem(description))
            self.steps_table.setItem(row, 2, QTableWidgetItem(status))
            self.steps_table.setItem(row, 3, QTableWidgetItem(str(order)))
            
            # Action buttons
            btn_delete = QPushButton("حذف")
            btn_delete.clicked.connect(lambda checked, sid=step_id: self.delete_step(sid))
            self.steps_table.setCellWidget(row, 4, btn_delete)

    def open_create_project(self):
        dlg = ProjectCreateDialog()
        if dlg.exec():
            values = dlg.get_values()
            if not values['title']:
                AppNotifier(QDialog).warning("خطا", "عنوان پروژه الزامی است")
            else:
                self.project_service.add(
                    self.idea_id, 
                    title=values['title'],
                    description=values['description'],
                    tech_stack=values['tech_stack'],
                    progress=values['progress'],
                    status=values['status'],
                    start_date=values['start_date'],
                    end_date=values['end_date']
                )
                self.load_projects()
    
    def open_create_step(self):
        if not self.current_project_id:
            AppNotifier(QDialog).warning("خطا", "لطفاً ابتدا یک پروژه انتخاب کنید")
            return
        dlg = ProjectStepCreateDialog()
        if dlg.exec():
            values = dlg.get_values()
            if not values['title']:
                AppNotifier(QDialog).warning("خطا", "عنوان مرحله الزامی است")
            else:
                self.step_service.add(
                    self.current_project_id,
                    title=values['title'],
                    description=values['description'],
                    order=values['order'],
                    status=values['status'],
                    start_date=values['start_date'],
                    end_date=values['end_date']
                )
                self.load_steps()
    
    def delete_step(self, step_id: str):
        if AppNotifier(QDialog).confirm("حذف", "آیا از حذف این مرحله مطمئن هستید؟"):
            self.step_service.delete(step_id)
            self.load_steps()

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
        self.setMinimumSize(500, 600)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        layout.addWidget(QLabel("عنوان *"))
        self.title_edit = QLineEdit()
        layout.addWidget(self.title_edit)
        
        layout.addWidget(QLabel("توضیحات"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(100)
        layout.addWidget(self.desc_edit)
        
        layout.addWidget(QLabel("تکنولوژی‌ها"))
        self.tech_stack_edit = QLineEdit()
        self.tech_stack_edit.setPlaceholderText("مثال: Python, Django, PostgreSQL")
        layout.addWidget(self.tech_stack_edit)
        
        layout.addWidget(QLabel("پیشرفت (0-100)"))
        self.progress_spin = QSpinBox()
        self.progress_spin.setRange(0, 100)
        self.progress_spin.setValue(0)
        layout.addWidget(self.progress_spin)
        
        layout.addWidget(QLabel("وضعیت"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["todo", "doing", "done"])
        layout.addWidget(self.status_combo)
        
        layout.addWidget(QLabel("تاریخ شروع"))
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.start_date_edit)
        
        layout.addWidget(QLabel("تاریخ پایان"))
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.end_date_edit)
        
        btns = QHBoxLayout()
        ok = QPushButton("ذخیره")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("انصراف")
        cancel.clicked.connect(self.reject)
        btns.addWidget(ok)
        btns.addWidget(cancel)
        layout.addLayout(btns)

    def get_values(self):
        return {
            'title': self.title_edit.text().strip(),
            'description': self.desc_edit.toPlainText().strip(),
            'tech_stack': self.tech_stack_edit.text().strip(),
            'progress': self.progress_spin.value(),
            'status': self.status_combo.currentText(),
            'start_date': self.start_date_edit.date().toPyDate(),
            'end_date': self.end_date_edit.date().toPyDate()
        }


class ProjectStepCreateDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("افزودن مرحله پروژه")
        self.setMinimumSize(500, 500)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        layout.addWidget(QLabel("عنوان *"))
        self.title_edit = QLineEdit()
        layout.addWidget(self.title_edit)
        
        layout.addWidget(QLabel("توضیحات"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(100)
        layout.addWidget(self.desc_edit)
        
        layout.addWidget(QLabel("ترتیب"))
        self.order_spin = QSpinBox()
        self.order_spin.setRange(0, 1000)
        self.order_spin.setValue(0)
        layout.addWidget(self.order_spin)
        
        layout.addWidget(QLabel("وضعیت"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["todo", "doing", "done"])
        layout.addWidget(self.status_combo)
        
        layout.addWidget(QLabel("تاریخ شروع"))
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.start_date_edit)
        
        layout.addWidget(QLabel("تاریخ پایان"))
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.end_date_edit)
        
        btns = QHBoxLayout()
        ok = QPushButton("ذخیره")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("انصراف")
        cancel.clicked.connect(self.reject)
        btns.addWidget(ok)
        btns.addWidget(cancel)
        layout.addLayout(btns)

    def get_values(self):
        return {
            'title': self.title_edit.text().strip(),
            'description': self.desc_edit.toPlainText().strip(),
            'order': self.order_spin.value(),
            'status': self.status_combo.currentText(),
            'start_date': self.start_date_edit.date().toPyDate(),
            'end_date': self.end_date_edit.date().toPyDate()
        }


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


