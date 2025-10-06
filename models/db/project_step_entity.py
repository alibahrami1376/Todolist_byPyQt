import uuid
from datetime import datetime, date

from sqlalchemy import String, DateTime, Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.db_session import Base


class ProjectStepEntity(Base):
    __tablename__ = "project_steps"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4().hex))
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    estimated_hours: Mapped[float] = mapped_column(Float, default=0.0)
    action_type: Mapped[str] = mapped_column(String(30), default="research")  # research | learning | coding | design | testing
    notes: Mapped[str] = mapped_column(String(4000), default="")
    status: Mapped[str] = mapped_column(String(30), default="planned")  # planned | in_progress | done
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())

    project: Mapped["ProjectEntity"] = relationship(back_populates="steps")


