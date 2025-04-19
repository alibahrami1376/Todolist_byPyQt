from typing import List, Optional
from models.task_models import TaskModel
from services.task_js_storage import TaskStorageService
from mapper.task_mapper import map_entity_to_model,map_model_to_entity

from services.task_service import TaskService

class TaskViewModel:
    def __init__(self,user_id: str):
        self.user_id = user_id
        self.TaskService = TaskService()
        self._tasks = [map_entity_to_model(e) for e in self.TaskService.get_tasks_by_user(user_id)]


    def get_all_tasks(self) :
        return self._tasks

    def add_task(self, task: TaskModel) -> None:
        entity = map_model_to_entity(task)
        entity.user_id = self.user_id  
        self.TaskService.add(entity)
        self._tasks.append(task)
        # TaskStorageService.append_task(task)

    def delete_task(self, task_id: str) -> None:
        self._tasks = [task for task in self._tasks if task.id != task_id]
        self.TaskService.delete(task_id)
        # TaskStorageService.delete_task(task_id)


    def update_task(self, updated_task: TaskModel) -> None:
        for i, task in enumerate(self._tasks):
            if task.id == updated_task.id:
                self._tasks[i] = updated_task
                break
            self.TaskService.update(map_model_to_entity(updated_task))
        # TaskStorageService.update_task(updated_task)

    def clear_all(self) -> None:
        self._tasks.clear()
        self.TaskService.clear_all_for_user(self.user_id)
        # TaskStorageService.delete_all()

    def find_by_id(self, task_id: str) -> Optional[TaskModel]:
        return next((task for task in self._tasks if task.id == task_id), None)

    def filter_by_priority(self, priority: str) -> List[TaskModel]:
        return [task for task in self._tasks if task.priority == priority]

    def get_subtasks(self, parent_id: str) -> List[TaskModel]:
        return [task for task in self._tasks if task.parent_id == parent_id]

    def mark_toggel(self, task_update: TaskModel, completed: bool) -> None:
        for i, task in enumerate(self._tasks):
            if task.id == task_update.id:
                self.TaskService.update_toggle_completed(map_model_to_entity(self._tasks[i] ), completed)
                self._tasks[i].completed = completed
                break
            
