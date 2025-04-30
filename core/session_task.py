from typing import List, Optional
from models.task_models import TaskModel
from PyQt6.QtCore import QObject,pyqtSignal

class TaskSession(QObject):
    _tasks: List[TaskModel] = []

    task_session_new= pyqtSignal(TaskModel)
    task_session_edit= pyqtSignal(TaskModel)
    task_session_remove= pyqtSignal()
    def __init__(self):
        super().__init__()



    def load_tasks(self, tasks: List[TaskModel]) -> None:
        """
        بارگذاری لیستی از تسک‌ها به درون حافظه
        """
        self._tasks = tasks.copy()


    def add_task(self, task: TaskModel) -> None:
        """
        اضافه کردن یک تسک به لیست حافظه
        """
        self._tasks.append(task)
        self.task_session_new.emit(task)

  
    def remove_task(self, task_id: str) -> None:
        """
        حذف یک تسک بر اساس شناسه
        """
        self._tasks = [task for task in self._tasks if task.id != task_id]
        self.task_session_remove.emit()
        

  
    def update_task(self, updated_task: TaskModel) -> None:
        """
        به‌روزرسانی یک تسک موجود در حافظه
        """
        for i, task in enumerate(self._tasks):
            if task.id == updated_task.id:
                self._tasks[i] = updated_task
                break
        self.task_session_edit.emit(updated_task)
 
    def get_all(self) -> List[TaskModel]:
        """
        گرفتن تمام تسک‌های موجود
        """
        return self._tasks.copy()


    def find_by_id(self, task_id: str) -> Optional[TaskModel]:
        """
        پیدا کردن یک تسک بر اساس شناسه
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None


    def clear(self) -> None:
        """
        پاک کردن تمام تسک‌های حافظه
        """
        self._tasks.clear()

  
    # def get_tasks_for_user(self, user_id: str) -> List[TaskModel]:
    #     """
    #     فیلتر کردن تسک‌ها بر اساس user_id
    #     """
    #     return [task for task in self._tasks if task.== user_id]

    def get_last_task(self)-> TaskModel:
        return self._tasks[-1]
    


    # Singleton instance to be used across the app
Task_Session = TaskSession()