import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.db_session import Base


class IdeaEntity(Base):
    __tablename__ = "ideas"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4().hex))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(1000), default="")
    goal: Mapped[str] = mapped_column(String(1000), default="")
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())

    projects: Mapped[list["ProjectEntity"]] = relationship(back_populates="idea", cascade="all, delete-orphan")
    category: Mapped["CategoryEntity"] = relationship(back_populates="ideas")
    answers: Mapped[list["AnswerEntity"]] = relationship(back_populates="idea", cascade="all, delete-orphan")
    insights: Mapped[list["InsightEntity"]] = relationship(back_populates="idea", cascade="all, delete-orphan")


