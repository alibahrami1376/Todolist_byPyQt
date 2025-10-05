import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.db_session import Base


class LearningPathEntity(Base):
    __tablename__ = "learning_paths"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4().hex))
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(String(4000), default="")
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())

    project: Mapped["ProjectEntity"] = relationship(back_populates="learning_paths")


