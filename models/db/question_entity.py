import uuid
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.db_session import Base


class QuestionEntity(Base):
    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4().hex))
    text: Mapped[str] = mapped_column(String(4000), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # coach | evaluate | roadmap
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id"), nullable=False)
    step: Mapped[int] = mapped_column(Integer, default=0)

    category: Mapped["CategoryEntity"] = relationship(back_populates="questions")
    answers: Mapped[list["AnswerEntity"]] = relationship(back_populates="question", cascade="all, delete-orphan")


