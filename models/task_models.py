import uuid
from datetime import datetime
from typing import Optional

class TaskModel:
    def __init__(
        self,
        title: str,
        description: str = "",
        priority: str = "متوسط",
        due_date: Optional[str] = None,
        completed: bool = False,
        is_subtask: bool = False,
        parent_id: Optional[str] = None,
        task_id: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id: str = task_id or uuid.uuid4().hex
        self.title: str = title
        self.description: str = description
        self.priority: str = priority
        self.due_date: str = due_date or datetime.now().strftime("%Y-%m-%d")
        self.completed: bool = completed
        self.is_subtask: bool = is_subtask
        self.parent_id: Optional[str] = parent_id
        self.created_at: str = created_at or datetime.now().isoformat()
        self.updated_at: str = updated_at or self.created_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed,
            "is_subtask": self.is_subtask,
            "parent_id": self.parent_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "TaskModel":
        return TaskModel(
            task_id=data.get("id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            priority=data.get("priority", "متوسط"),
            due_date=data.get("due_date"),
            completed=data.get("completed", False),
            is_subtask=data.get("is_subtask", False),
            parent_id=data.get("parent_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
