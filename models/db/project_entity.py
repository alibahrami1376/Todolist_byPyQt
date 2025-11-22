import uuid
from datetime import datetime, date

from sqlalchemy import String, DateTime, Date, Float, ForeignKey, Integer, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from services.db_session import Base


class ProjectStatusEnum(str, enum.Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class ProjectEntity(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default=lambda: str(uuid.uuid4().hex))
    idea_id: Mapped[str] = mapped_column(ForeignKey("ideas.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    tech_stack: Mapped[str] = mapped_column(String(300), nullable=True)
    progress: Mapped[int] = mapped_column(Integer, default=0)  # 0-100
    status: Mapped[str] = mapped_column(String(20), default="todo")  # todo, doing, done
    start_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())
    
    # Keep old fields for backward compatibility
    summary: Mapped[str] = mapped_column(String(2000), default="", nullable=True)
    estimated_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=True)
    priority: Mapped[str] = mapped_column(String(20), default="medium", nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow(), nullable=True)

    idea: Mapped["IdeaEntity"] = relationship(back_populates="projects")
    learning_paths: Mapped[list["LearningPathEntity"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    steps: Mapped[list["ProjectStepEntity"]] = relationship(back_populates="project", cascade="all, delete-orphan")


