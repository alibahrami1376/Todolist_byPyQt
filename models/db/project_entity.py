import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.db_session import Base


class ProjectEntity(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4().hex))
    idea_id: Mapped[str] = mapped_column(ForeignKey("ideas.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), default="")
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())

    idea: Mapped["IdeaEntity"] = relationship(back_populates="projects")
    learning_paths: Mapped[list["LearningPathEntity"]] = relationship(back_populates="project", cascade="all, delete-orphan")


