from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QHBoxLayout, QCheckBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPalette, QColor

from models.task_models import TaskModel
from viewmodels.task_view_models import TaskViewModel
from views.view_addtask import AddTaskWindow

class TaskManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager - Todo List")
        self.setFixedSize(450, 600)
        self.setWindowIcon(QIcon('images/checklist.png')) 

        self.viewmodel = TaskViewModel()

        self.set_dark_theme()
        self.init_ui()
        self.load_tasks()

    def set_dark_theme(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setPalette(palette)

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        add_btn = QPushButton("➕ افزودن")
        add_btn.clicked.connect(self.open_add_task_window)

        remove_btn = QPushButton("❌ حذف انتخاب‌شده")
        remove_btn.clicked.connect(self.remove_selected_task)

        clear_btn = QPushButton("🗑️ حذف همه")
        clear_btn.clicked.connect(self.clear_all_tasks)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(remove_btn)
        btn_layout.addWidget(clear_btn)

        layout.addLayout(btn_layout)
        self.setCentralWidget(central_widget)

    def load_tasks(self):
        self.task_list.clear()
        for task in self.viewmodel.get_all_tasks():
            self.add_task_to_ui(task)

    def add_task_to_ui(self, task: TaskModel):
        item = QListWidgetItem()
        checkbox = QCheckBox(f"{task.title} | اولویت: {task.priority} | سررسید: {task.due_date}")
        checkbox.setChecked(task.completed)
        checkbox.stateChanged.connect(lambda state, t=task: self.toggle_complete(t, state))
        font = checkbox.font()
        font.setStrikeOut(task.completed)
        checkbox.setFont(font)

        item.setSizeHint(checkbox.sizeHint())
        item.setData(Qt.ItemDataRole.UserRole, task.id)
        self.task_list.addItem(item)
        self.task_list.setItemWidget(item, checkbox)

    def open_add_task_window(self):
        window = AddTaskWindow(self)
        if window.exec():
            # دریافت تسک از فرم اضافه‌سازی
            task = window.task_data  # این فرض بر این است که فرم task_data را به‌روزرسانی کرده باشد
            if task:
                self.viewmodel.add_task(TaskModel(**task))
                self.load_tasks()

    def remove_selected_task(self):
        item = self.task_list.currentItem()
        if not item:
            QMessageBox.warning(self, "خطا", "تسکی انتخاب نشده است.")
            return

        task_id = item.data(Qt.ItemDataRole.UserRole)
        self.viewmodel.delete_task(task_id)
        self.load_tasks()

    def clear_all_tasks(self):
        confirm = QMessageBox.question(self, "تأیید حذف", "آیا مطمئن هستید که می‌خواهید همه تسک‌ها حذف شوند؟")
        if confirm == QMessageBox.StandardButton.Yes:
            self.viewmodel.clear_all()
            self.load_tasks()

    def toggle_complete(self, task: TaskModel, state):
        task.completed = bool(state)
        self.viewmodel.update_task(task)
        self.load_tasks()
