# mappers/task_mapper.py

from models.db.task_entity import TaskEntity
from models.task_models import TaskModel
from datetime import date
def map_entity_to_model(entity: TaskEntity) -> TaskModel:
    return TaskModel(
        task_id=entity.id,
        title=entity.title,
        description=entity.description,
        priority=entity.priority,
        due_date=entity.due_date,
        is_subtask=entity.is_subtask,
        completed=entity.completed
    )


def map_model_to_entity(model: TaskModel) -> TaskEntity:
    return TaskEntity(
        id=model.id,
        title=model.title,
        description=model.description,
        priority=model.priority,
        due_date=model.due_date if isinstance(model.due_date, date) else date.fromisoformat(model.due_date),
        is_subtask=model.is_subtask,
        completed=model.completed
    )


def map_model_to_entity_by_userid(model: TaskModel,userid: str) -> TaskEntity:
    return TaskEntity(
        id= model.id,
        title= model.title,
        description= model.description,
        priority= model.priority,
        due_date= model.due_date if isinstance(model.due_date, date) else date.fromisoformat(model.due_date),
        is_subtask= model.is_subtask,
        completed= model.completed,
        user_id= userid
    )

