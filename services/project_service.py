from typing import List, Tuple, Optional
from sqlalchemy import select
from datetime import date

from services.db_session import get_session
from models.db.project_entity import ProjectEntity


class ProjectService:
    def list_all(self) -> List[Tuple[str, str, str, str, str]]:
        with get_session() as db:
            rows = db.scalars(select(ProjectEntity).order_by(ProjectEntity.created_at.desc())).all()
            return [
                (p.id, p.title, p.description or p.summary or "", p.status, p.created_at.isoformat())
                for p in rows
            ]
    
    def list_by_idea(self, idea_id: str) -> List[Tuple[str, str, str, str, str, int, str]]:
        with get_session() as db:
            rows = db.scalars(
                select(ProjectEntity).where(ProjectEntity.idea_id == idea_id).order_by(ProjectEntity.created_at.desc())
            ).all()
            return [
                (p.id, p.title, p.description or "", p.status, p.created_at.isoformat(), p.progress or 0, p.id)
                for p in rows
            ]

    def add(self, idea_id: str, title: str, description: str = "", tech_stack: str = "", 
            progress: int = 0, status: str = "todo", start_date: Optional[date] = None, 
            end_date: Optional[date] = None) -> str:
        from uuid import uuid4
        with get_session() as db:
            pid = uuid4().hex
            project = ProjectEntity(
                id=pid, 
                idea_id=idea_id, 
                title=title, 
                description=description,
                tech_stack=tech_stack,
                progress=progress,
                status=status,
                start_date=start_date,
                end_date=end_date
            )
            db.add(project)
            db.commit()
            return pid

    def get(self, project_id: str) -> Optional[ProjectEntity]:
        with get_session() as db:
            return db.get(ProjectEntity, project_id)

    def delete(self, project_id: str) -> None:
        with get_session() as db:
            obj = db.get(ProjectEntity, project_id)
            if obj:
                db.delete(obj)
                db.commit()


