from typing import List, Optional
from datetime import date, datetime
from sqlalchemy import select, update, delete
from services.db_session import get_session, Base, engine
from models.db.course_entity import CourseEntity


class CourseService:
    def __init__(self):
        # جداول به صورت خودکار در init_db ایجاد می‌شوند
        pass

    def create_course(
        self,
        title: str,
        description: Optional[str] = None,
        start_date: Optional[date] = None,
        link: Optional[str] = None,
        status: str = "در حال انجام"
    ) -> str:
        """ایجاد دوره جدید"""
        with get_session() as db:
            course = CourseEntity(
                title=title,
                description=description,
                start_date=start_date,
                link=link,
                status=status
            )
            db.add(course)
            db.commit()
            db.refresh(course)
            return course.id

    def get_all_courses(self) -> List[CourseEntity]:
        """دریافت همه دوره‌ها"""
        with get_session() as db:
            stmt = select(CourseEntity).order_by(CourseEntity.created_at.desc())
            result = db.execute(stmt)
            courses = list(result.scalars().all())
            for course in courses:
                db.expunge(course)
            return courses

    def get_course_by_id(self, course_id: str) -> Optional[CourseEntity]:
        """دریافت دوره بر اساس ID"""
        with get_session() as db:
            stmt = select(CourseEntity).where(CourseEntity.id == course_id)
            result = db.execute(stmt)
            return result.scalar_one_or_none()

    def update_course(
        self,
        course_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        start_date: Optional[date] = None,
        link: Optional[str] = None,
        status: Optional[str] = None
    ) -> bool:
        """به‌روزرسانی دوره"""
        with get_session() as db:
            course = db.execute(
                select(CourseEntity).where(CourseEntity.id == course_id)
            ).scalar_one_or_none()
            
            if not course:
                return False
            
            if title is not None:
                course.title = title
            if description is not None:
                course.description = description
            if start_date is not None:
                course.start_date = start_date
            if link is not None:
                course.link = link
            if status is not None:
                course.status = status
            
            course.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(course)
            return True

    def delete_course(self, course_id: str) -> bool:
        """حذف دوره"""
        with get_session() as db:
            stmt = delete(CourseEntity).where(CourseEntity.id == course_id)
            result = db.execute(stmt)
            db.commit()
            return result.rowcount > 0

