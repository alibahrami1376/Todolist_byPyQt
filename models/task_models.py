import uuid
from datetime import date
from typing import Optional
from datetime import date,datetime

class TaskModel:
    def __init__(
        self,
        title: str,
        description: str = "",
        priority: str = "midel",
        due_date: Optional[date]= None,
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
        self.due_date: date = due_date or date.today()
        self.completed: bool = completed
        self.is_subtask: bool = is_subtask
        self.parent_id: Optional[str] = parent_id
        self.created_at: str = created_at or date.today().isoformat()
        self.updated_at: str = updated_at or self.created_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
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
            due_date=date.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            completed=data.get("completed", False),
            is_subtask=data.get("is_subtask", False),
            parent_id=data.get("parent_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
