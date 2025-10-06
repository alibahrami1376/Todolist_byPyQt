import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.db_session import Base


class CategoryEntity(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4().hex))
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(2000), default="")

    ideas: Mapped[list["IdeaEntity"]] = relationship(back_populates="category", cascade="all, delete-orphan")
    questions: Mapped[list["QuestionEntity"]] = relationship(back_populates="category", cascade="all, delete-orphan")


