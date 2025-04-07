from typing import List, Optional
from models.task_models import TaskModel
from services.task_storage_service import TaskStorageService

class TaskViewModel:
    def __init__(self):
        self._tasks: List[TaskModel] = TaskStorageService.load_all()

    def get_all_tasks(self) -> List[TaskModel]:
        return self._tasks

    def add_task(self, task: TaskModel) -> None:
        self._tasks.append(task)
        TaskStorageService.append_task(task)

    def delete_task(self, task_id: str) -> None:
        self._tasks = [task for task in self._tasks if task.id != task_id]
        TaskStorageService.delete_task(task_id)

    def update_task(self, updated_task: TaskModel) -> None:
        for i, task in enumerate(self._tasks):
            if task.id == updated_task.id:
                self._tasks[i] = updated_task
                break
        TaskStorageService.update_task(updated_task)

    def clear_all(self) -> None:
        self._tasks.clear()
        TaskStorageService.delete_all()

    def find_by_id(self, task_id: str) -> Optional[TaskModel]:
        return next((task for task in self._tasks if task.id == task_id), None)

    def filter_by_priority(self, priority: str) -> List[TaskModel]:
        return [task for task in self._tasks if task.priority == priority]

    def get_subtasks(self, parent_id: str) -> List[TaskModel]:
        return [task for task in self._tasks if task.parent_id == parent_id]

    def mark_complete(self, task_id: str, completed: bool) -> None:
        task = self.find_by_id(task_id)
        if task:
            task.completed = completed
            self.update_task(task)
