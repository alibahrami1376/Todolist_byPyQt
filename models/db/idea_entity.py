import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, Integer, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from services.db_session import Base


class PriorityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class IdeaEntity(Base):
    __tablename__ = "ideas"

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default=lambda: str(uuid.uuid4().hex))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)  # Simple category name
    tags: Mapped[str] = mapped_column(String(300), nullable=True)
    priority: Mapped[str] = mapped_column(String(20), default="medium")  # low, medium, high
    score: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())
    
    # Keep old fields for backward compatibility
    summary: Mapped[str] = mapped_column(String(1000), default="", nullable=True)
    goal: Mapped[str] = mapped_column(String(1000), default="", nullable=True)
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="draft", nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow(), nullable=True)

    projects: Mapped[list["ProjectEntity"]] = relationship(back_populates="idea", cascade="all, delete-orphan")
    category_relation: Mapped["CategoryEntity"] = relationship(back_populates="ideas", foreign_keys=[category_id])
    answers: Mapped[list["AnswerEntity"]] = relationship(back_populates="idea", cascade="all, delete-orphan")
    insights: Mapped[list["InsightEntity"]] = relationship(back_populates="idea", cascade="all, delete-orphan")


