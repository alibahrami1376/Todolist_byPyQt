from typing import List, Tuple
from sqlalchemy import select

from services.db_session import get_session
from models.db.learning_path_entity import LearningPathEntity


class LearningPathService:
    def list_by_project(self, project_id: str) -> List[Tuple[str, str, str, int, str]]:
        with get_session() as db:
            rows = db.scalars(
                select(LearningPathEntity)
                .where(LearningPathEntity.project_id == project_id)
                .order_by(LearningPathEntity.order_index.asc())
            ).all()
            return [
                (lp.id, lp.title, lp.content, lp.order_index, lp.created_at.isoformat())
                for lp in rows
            ]

    def add(self, project_id: str, title: str, content: str = "", order_index: int = 0) -> str:
        from uuid import uuid4
        with get_session() as db:
            lid = uuid4().hex
            db.add(
                LearningPathEntity(
                    id=lid,
                    project_id=project_id,
                    title=title,
                    content=content,
                    order_index=order_index,
                )
            )
            db.commit()
            return lid

    def delete(self, learning_path_id: str) -> None:
        with get_session() as db:
            obj = db.get(LearningPathEntity, learning_path_id)
            if obj:
                db.delete(obj)
                db.commit()


