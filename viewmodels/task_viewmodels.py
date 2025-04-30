from typing import List, Optional
from models.task_models import TaskModel
from services.task_js_storage import TaskJsonStorage
from mapper.task_mapper import map_model_to_entity_by_userid,map_entity_to_model,map_model_to_entity

from services.task_service import TaskService
from core.session_manager import Session
from core.session_task import Task_Session
from services.task_js_storage import TaskJsonStorage
class TaskViewModel:
    def __init__(self,):
        self.TaskService= TaskService()
        self.TaskJsonStorage= TaskJsonStorage() 


    def get_all_tasks(self,user_id: str) :
        return [map_entity_to_model(e) for e in self.TaskService.get_tasks_by_user(user_id)]

    def get_all_tasks_jason(self) -> List[TaskModel]:
        return self.TaskJsonStorage.load_all()

    def add_task_quick(self,titel: str):
        task = self.creat_quick_task(titel)
        if not Session.is_guest():
            self.TaskService.add(map_model_to_entity_by_userid(task,Session.get_id_user()))
        Task_Session.add_task(task)
        
    def creat_quick_task(self,titel: str):
        return TaskModel(titel)
    
    def creat_task(self,task : TaskModel):
        if not Session.is_guest():
            self.TaskService.add(map_model_to_entity_by_userid(task,Session.get_id_user()))
        Task_Session.add_task(task)

    # def add_task(self, task: TaskModel) -> None:
    #     entity = map_model_to_entity(task)
    #     entity.user_id = self.user_id  
    #     self.TaskService.add(entity)
    #     self._tasks.append(task)
    #     # TaskStorageService.append_task(task)

    def delete_task(self, task: TaskModel) -> None:
        task_id = task.id
        if  not Session.is_guest():
            self.TaskService.delete(task_id)
        Task_Session.remove_task(task_id)
        #TaskStorageService.delete_task(task_id)


    def update_task(self, updated_task: TaskModel) -> None:
       
        Task_Session.update_task(updated_task)
        if  not Session.is_guest():
            self.TaskService.update(map_model_to_entity(updated_task))
        # 

    def save_tasks_jason(self):
        self.TaskJsonStorage.save_all(Task_Session.get_all())

    # def clear_all(self) -> None:
    #     self._tasks.clear()
    #     self.TaskService.clear_all_for_user(self.user_id)
    #     # TaskStorageService.delete_all()

    # def find_by_id(self, task_id: str) -> Optional[TaskModel]:
    #     return next((task for task in self._tasks if task.id == task_id), None)

    # def filter_by_priority(self, priority: str) -> List[TaskModel]:
    #     return [task for task in self._tasks if task.priority == priority]

    # def get_subtasks(self, parent_id: str) -> List[TaskModel]:
    #     return [task for task in self._tasks if task.parent_id == parent_id]

    # def mark_toggel(self, task_update: TaskModel, completed: bool) -> None:
    #     for i, task in enumerate(self._tasks):
    #         if task.id == task_update.id:
    #             self.TaskService.update_toggle_completed(map_model_to_entity(self._tasks[i] ), completed)
    #             self._tasks[i].completed = completed
    #             break
            
