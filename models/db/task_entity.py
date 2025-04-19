import uuid


from sqlalchemy import String, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from services.db_session import Base

from sqlalchemy import Date


class TaskEntity(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), default="")
    priority: Mapped[str] = mapped_column(String(20), default="middle")
    due_date: Mapped[Date] = mapped_column(Date, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_subtask: Mapped[bool] = mapped_column(Boolean, default=False)
    parent_id: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["UserEntity"] = relationship(back_populates="tasks")
