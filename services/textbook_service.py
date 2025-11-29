from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, update, delete
from services.db_session import get_session, Base, engine
from models.db.course_entity import TextbookEntity, LearningLoopEntity


class TextbookService:
    def __init__(self):
        # جداول به صورت خودکار در init_db ایجاد می‌شوند
        pass

    def create_textbook(
        self,
        title: str,
        content: Optional[str] = None,
        course_id: Optional[str] = None,
        link: Optional[str] = None,
        progress: float = 0.0
    ) -> str:
        """ایجاد کتاب درسی جدید"""
        with get_session() as db:
            textbook = TextbookEntity(
                title=title,
                content=content,
                course_id=course_id,
                link=link,
                progress=progress
            )
            db.add(textbook)
            db.commit()
            db.refresh(textbook)
            return textbook.id

    def get_all_textbooks(self, course_id: Optional[str] = None) -> List[TextbookEntity]:
        """دریافت همه کتاب‌های درسی"""
        with get_session() as db:
            stmt = select(TextbookEntity)
            if course_id:
                stmt = stmt.where(TextbookEntity.course_id == course_id)
            stmt = stmt.order_by(TextbookEntity.created_at.desc())
            result = db.execute(stmt)
            textbooks = list(result.scalars().all())
            for textbook in textbooks:
                db.expunge(textbook)
            return textbooks

    def get_textbook_by_id(self, textbook_id: str) -> Optional[TextbookEntity]:
        """دریافت کتاب درسی بر اساس ID"""
        with get_session() as db:
            stmt = select(TextbookEntity).where(TextbookEntity.id == textbook_id)
            result = db.execute(stmt)
            return result.scalar_one_or_none()

    def update_textbook(
        self,
        textbook_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        course_id: Optional[str] = None,
        link: Optional[str] = None,
        progress: Optional[float] = None
    ) -> bool:
        """به‌روزرسانی کتاب درسی"""
        with get_session() as db:
            textbook = db.execute(
                select(TextbookEntity).where(TextbookEntity.id == textbook_id)
            ).scalar_one_or_none()
            
            if not textbook:
                return False
            
            if title is not None:
                textbook.title = title
            if content is not None:
                textbook.content = content
            if course_id is not None:
                textbook.course_id = course_id
            if link is not None:
                textbook.link = link
            if progress is not None:
                textbook.progress = progress
            
            textbook.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(textbook)
            return True

    def delete_textbook(self, textbook_id: str) -> bool:
        """حذف کتاب درسی"""
        with get_session() as db:
            stmt = delete(TextbookEntity).where(TextbookEntity.id == textbook_id)
            result = db.execute(stmt)
            db.commit()
            return result.rowcount > 0

    def get_learning_loops(self, textbook_id: str) -> List[LearningLoopEntity]:
        """دریافت حلقه‌های یادگیری یک کتاب"""
        with get_session() as db:
            stmt = select(LearningLoopEntity).where(
                LearningLoopEntity.textbook_id == textbook_id
            ).order_by(LearningLoopEntity.created_at.desc())
            result = db.execute(stmt)
            loops = list(result.scalars().all())
            for loop in loops:
                db.expunge(loop)
            return loops

    def create_learning_loop(
        self,
        textbook_id: str,
        title: str,
        content: Optional[str] = None,
        completed: bool = False
    ) -> str:
        """ایجاد حلقه یادگیری جدید"""
        with get_session() as db:
            loop = LearningLoopEntity(
                textbook_id=textbook_id,
                title=title,
                content=content,
                completed=completed
            )
            db.add(loop)
            db.commit()
            db.refresh(loop)
            return loop.id

    def update_learning_loop(
        self,
        loop_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> bool:
        """به‌روزرسانی حلقه یادگیری"""
        with get_session() as db:
            loop = db.execute(
                select(LearningLoopEntity).where(LearningLoopEntity.id == loop_id)
            ).scalar_one_or_none()
            
            if not loop:
                return False
            
            if title is not None:
                loop.title = title
            if content is not None:
                loop.content = content
            if completed is not None:
                loop.completed = completed
            
            loop.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(loop)
            return True

    def delete_learning_loop(self, loop_id: str) -> bool:
        """حذف حلقه یادگیری"""
        with get_session() as db:
            stmt = delete(LearningLoopEntity).where(LearningLoopEntity.id == loop_id)
            result = db.execute(stmt)
            db.commit()
            return result.rowcount > 0

