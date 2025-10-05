from typing import List, Tuple
from sqlalchemy import select

from services.db_session import get_session
from models.db.project_entity import ProjectEntity


class ProjectService:
    def list_by_idea(self, idea_id: str) -> List[Tuple[str, str, str, str, str]]:
        with get_session() as db:
            rows = db.scalars(
                select(ProjectEntity).where(ProjectEntity.idea_id == idea_id).order_by(ProjectEntity.created_at.desc())
            ).all()
            return [
                (p.id, p.title, p.description, p.status, p.created_at.isoformat())
                for p in rows
            ]

    def add(self, idea_id: str, title: str, description: str = "", status: str = "pending") -> str:
        from uuid import uuid4
        with get_session() as db:
            pid = uuid4().hex
            db.add(ProjectEntity(id=pid, idea_id=idea_id, title=title, description=description, status=status))
            db.commit()
            return pid

    def delete(self, project_id: str) -> None:
        with get_session() as db:
            obj = db.get(ProjectEntity, project_id)
            if obj:
                db.delete(obj)
                db.commit()


