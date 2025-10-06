import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.db_session import Base


class InsightEntity(Base):
    __tablename__ = "insights"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4().hex))
    idea_id: Mapped[str] = mapped_column(ForeignKey("ideas.id"), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # recommendation | roadmap_step
    text: Mapped[str] = mapped_column(String(4000), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())

    idea: Mapped["IdeaEntity"] = relationship(back_populates="insights")


