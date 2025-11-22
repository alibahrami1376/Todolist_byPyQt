import uuid
from datetime import datetime, date

from sqlalchemy import String, DateTime, Date, Float, ForeignKey, Integer, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from services.db_session import Base


class StepStatusEnum(str, enum.Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class ProjectStepEntity(Base):
    __tablename__ = "project_steps"

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default=lambda: str(uuid.uuid4().hex))
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="todo")  # todo, doing, done
    start_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    
    # Keep old fields for backward compatibility
    estimated_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=True)
    action_type: Mapped[str] = mapped_column(String(30), default="research", nullable=True)
    notes: Mapped[str] = mapped_column(String(4000), default="", nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow(), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow(), nullable=True)

    project: Mapped["ProjectEntity"] = relationship(back_populates="steps")


