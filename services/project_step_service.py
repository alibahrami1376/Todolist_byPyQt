from typing import List, Tuple, Optional
from sqlalchemy import select
from datetime import date

from services.db_session import get_session
from models.db.project_step_entity import ProjectStepEntity


class ProjectStepService:
    def list_by_project(self, project_id: str) -> List[Tuple[str, str, str, str, int]]:
        with get_session() as db:
            rows = db.scalars(
                select(ProjectStepEntity)
                .where(ProjectStepEntity.project_id == project_id)
                .order_by(ProjectStepEntity.order.asc(), ProjectStepEntity.created_at.asc())
            ).all()
            return [
                (p.id, p.title, p.description or "", p.status, p.order)
                for p in rows
            ]

    def add(self, project_id: str, title: str, description: str = "", 
            order: int = 0, status: str = "todo", 
            start_date: Optional[date] = None, end_date: Optional[date] = None) -> str:
        from uuid import uuid4
        with get_session() as db:
            step_id = uuid4().hex
            step = ProjectStepEntity(
                id=step_id,
                project_id=project_id,
                title=title,
                description=description,
                order=order,
                status=status,
                start_date=start_date,
                end_date=end_date
            )
            db.add(step)
            db.commit()
            return step_id

    def get(self, step_id: str) -> Optional[ProjectStepEntity]:
        with get_session() as db:
            return db.get(ProjectStepEntity, step_id)

    def delete(self, step_id: str) -> None:
        with get_session() as db:
            obj = db.get(ProjectStepEntity, step_id)
            if obj:
                db.delete(obj)
                db.commit()

    def update_status(self, step_id: str, status: str) -> None:
        with get_session() as db:
            obj = db.get(ProjectStepEntity, step_id)
            if obj:
                obj.status = status
                db.commit()

    def update(self, step_id: str, title: str = None, description: str = None, 
               status: str = None, order: int = None) -> bool:
        with get_session() as db:
            obj = db.get(ProjectStepEntity, step_id)
            if not obj:
                return False
            if title is not None:
                obj.title = title
            if description is not None:
                obj.description = description
            if status is not None:
                obj.status = status
            if order is not None:
                obj.order = order
            db.commit()
            return True

    def reorder(self, project_id: str, ordered_ids: List[str]) -> None:
        with get_session() as db:
            steps = db.scalars(
                select(ProjectStepEntity).where(ProjectStepEntity.project_id == project_id)
            ).all()
            step_map = {step.id: step for step in steps}
            for order_index, step_id in enumerate(ordered_ids, start=1):
                step = step_map.get(step_id)
                if step:
                    step.order = order_index
            db.commit()

