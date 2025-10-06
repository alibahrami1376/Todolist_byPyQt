import uuid
from datetime import datetime, date

from sqlalchemy import String, DateTime, Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.db_session import Base


class ProjectEntity(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4().hex))
    idea_id: Mapped[str] = mapped_column(ForeignKey("ideas.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(2000), default="")
    start_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    estimated_hours: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="planned")  # planned | in_progress | completed | paused
    priority: Mapped[str] = mapped_column(String(20), default="medium")  # low | medium | high
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())

    idea: Mapped["IdeaEntity"] = relationship(back_populates="projects")
    learning_paths: Mapped[list["LearningPathEntity"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    steps: Mapped[list["ProjectStepEntity"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    columns: Mapped[list["ColumnEntity"]] = relationship(back_populates="project", cascade="all, delete-orphan")

