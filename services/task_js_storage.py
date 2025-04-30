import json
import os
from typing import List
from models.task_models import TaskModel

class TaskJsonStorage:

    FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'tasks.json')
    
    @classmethod
    def save_all(cls, tasks: List[TaskModel]) -> None:
        with open(cls.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in tasks], file, ensure_ascii=False, indent=4)

    @classmethod
    def load_all(cls) -> List[TaskModel]:
        if not os.path.exists(cls.FILE_PATH):
            return []

        with open(cls.FILE_PATH, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                return [TaskModel.from_dict(task_data) for task_data in data]
            except json.JSONDecodeError:
                return []

    @classmethod
    def delete_all(cls) -> None:
        if os.path.exists(cls.FILE_PATH):
            os.remove(cls.FILE_PATH)

    @classmethod
    def append_task(cls, task: TaskModel) -> None:
        tasks = cls.load_all()
        tasks.append(task)
        cls.save_all(tasks)

    @classmethod
    def update_task(cls, updated_task: TaskModel) -> None:
        tasks = cls.load_all()
        for i, task in enumerate(tasks):
            if task.id == updated_task.id:
                tasks[i] = updated_task
                break
        cls.save_all(tasks)

    @classmethod
    def delete_task(cls, task_id: str) -> None:
        tasks = cls.load_all()
        tasks = [task for task in tasks if task.id != task_id]
        cls.save_all(tasks)





