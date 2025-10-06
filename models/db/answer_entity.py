import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.db_session import Base


class AnswerEntity(Base):
    __tablename__ = "answers"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4().hex))
    idea_id: Mapped[str] = mapped_column(ForeignKey("ideas.id"), nullable=False)
    question_id: Mapped[str] = mapped_column(ForeignKey("questions.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(4000), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow())

    idea: Mapped["IdeaEntity"] = relationship(back_populates="answers")
    question: Mapped["QuestionEntity"] = relationship(back_populates="answers")


