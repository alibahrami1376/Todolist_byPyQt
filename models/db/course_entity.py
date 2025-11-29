import uuid
from datetime import date, datetime
from typing import Optional
from sqlalchemy import String, Date, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from services.db_session import Base


class CourseEntity(Base):
    __tablename__ = "courses"

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default=lambda: str(uuid.uuid4().hex))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    link: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="در حال انجام")  # در حال انجام، تکمیل شده، متوقف شده
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    
    # Relationships
    textbooks: Mapped[list["TextbookEntity"]] = relationship(back_populates="course", cascade="all, delete-orphan")
    documents: Mapped[list["DocumentEntity"]] = relationship(back_populates="course", cascade="all, delete-orphan")


class TextbookEntity(Base):
    __tablename__ = "textbooks"

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default=lambda: str(uuid.uuid4().hex))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    course_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("courses.id"), nullable=True)  # اختیاری
    link: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    progress: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # درصد پیشرفت
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    
    # Relationships
    course: Mapped[Optional["CourseEntity"]] = relationship(back_populates="textbooks")
    learning_loops: Mapped[list["LearningLoopEntity"]] = relationship(back_populates="textbook", cascade="all, delete-orphan")
    documents: Mapped[list["DocumentEntity"]] = relationship(back_populates="textbook", cascade="all, delete-orphan")


class LearningLoopEntity(Base):
    __tablename__ = "learning_loops"

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default=lambda: str(uuid.uuid4().hex))
    textbook_id: Mapped[str] = mapped_column(String(50), ForeignKey("textbooks.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    
    # Relationships
    textbook: Mapped["TextbookEntity"] = relationship(back_populates="learning_loops")

