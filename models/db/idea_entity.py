import uuid
from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from services.db_session import Base


class IdeaEntity(Base):
    __tablename__ = "ideas"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4().hex))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())


