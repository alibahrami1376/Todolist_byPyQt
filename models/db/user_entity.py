import uuid

from sqlalchemy.orm import relationship
from services.db_session import Base
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column



class UserEntity(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    tasks: Mapped[list["TaskEntity"]] = relationship(back_populates="user", cascade="all, delete-orphan")