from typing import List, Tuple
from sqlalchemy import select
from services.db_session import get_session, Base, engine
from models.db.idea_entity import IdeaEntity
from models.db.project_entity import ProjectEntity  # ensure mapper is loaded
from models.db.learning_path_entity import LearningPathEntity  # ensure mapper is loaded


class IdeaService:
    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def list_ideas(self) -> List[Tuple[str, str, str, str]]:
        with get_session() as db:
            rows = db.scalars(select(IdeaEntity).order_by(IdeaEntity.created_at.desc())).all()
            return [
                (r.id, r.title, r.summary, r.created_at.isoformat())
                for r in rows
            ]

    def add_idea(self, id_value: str, title: str, summary: str, goal: str) -> None:
        with get_session() as db:
            idea = IdeaEntity(id=id_value, title=title, summary=summary, goal=goal)
            db.add(idea)
            db.commit()

    def delete_idea(self, id_value: str) -> None:
        with get_session() as db:
            obj = db.get(IdeaEntity, id_value)
            if obj:
                db.delete(obj)
                db.commit()

    def get_idea(self, id_value: str) -> Tuple[str, str, str, str, str]:
        with get_session() as db:
            obj = db.get(IdeaEntity, id_value)
            if not obj:
                raise ValueError("Idea not found")
            return (obj.id, obj.title, obj.summary, obj.goal, obj.created_at.isoformat())


