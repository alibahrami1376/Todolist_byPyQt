
from typing import List

from models.db.task_entity import TaskEntity

from services.db_session import get_session

class TaskService:
    def __init__(self):
        pass    
    def get_all(self) -> List[TaskEntity]:
        with get_session() as db :
            return db.query(TaskEntity).all()

    def get_tasks_by_user(self, user_id: str) -> List[TaskEntity]:
         with get_session() as db :
            return db.query(TaskEntity).filter(TaskEntity.user_id == user_id).all()
    

    def get_by_user(self, user_id: str) -> List[TaskEntity]:
         with get_session() as db :
            return db.query(TaskEntity).filter(TaskEntity.user_id == user_id).all()

    def add(self, task: TaskEntity):
         with get_session() as db :
            db.add(task)
            db.commit()
            db.refresh(task)
            return task

    def update(self,updated_task: TaskEntity):
         with get_session() as db :
            task = db.query(TaskEntity).filter_by(id=updated_task.id).first()
            task.title = updated_task.title
            task.description = updated_task.description
            task.due_date = updated_task.due_date
            task.completed = updated_task.completed
            task.priority = updated_task.priority
            task.is_subtask = updated_task.is_subtask
            task.parent_id = updated_task.parent_id
            db.commit()
    def update_toggle_completed(self, updated_task: TaskEntity, completed: bool):
            with get_session() as db :
                task = db.query(TaskEntity).filter_by(id=updated_task.id).first()
                task.completed = completed
                db.commit()   

    def delete(self, task_id: str):
        with get_session() as db :
            task = db.get(TaskEntity, task_id)
            if task:
                db.delete(task)
                db.commit()

    def clear_all_for_user(self, user_id: str):
         with get_session() as db :
            db.query(TaskEntity).filter(TaskEntity.user_id == user_id).delete()
            db.commit()



