from typing import List, Tuple
from sqlalchemy import select
from services.db_session import get_session, Base, engine
from models.db.idea_entity import IdeaEntity


class IdeaService:
    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def list_ideas(self) -> List[Tuple[str, str, str, str]]:
        with get_session() as db:
            rows = db.scalars(select(IdeaEntity).order_by(IdeaEntity.created_at.desc())).all()
            return [
                (r.id, r.title, r.description, r.created_at.isoformat())
                for r in rows
            ]

    def add_idea(self, id_value: str, title: str, description: str) -> None:
        with get_session() as db:
            idea = IdeaEntity(id=id_value, title=title, description=description)
            db.add(idea)
            db.commit()

    def delete_idea(self, id_value: str) -> None:
        with get_session() as db:
            obj = db.get(IdeaEntity, id_value)
            if obj:
                db.delete(obj)
                db.commit()


