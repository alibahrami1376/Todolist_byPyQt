from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase,Session

from contextlib import contextmanager
from typing import Generator
DATABASE_URL = "sqlite:///data/tasks.db"


class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)






@contextmanager
def get_session() -> Generator[Session,None,None]:
    """Context-managed session for safe open/close."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    """Import all models and create database tables if missing."""
    # Import all entity modules so SQLAlchemy registers mappers before create_all
    from models.db.user_entity import UserEntity  # noqa: F401
    from models.db.task_entity import TaskEntity  # noqa: F401
    from models.db.idea_entity import IdeaEntity  # noqa: F401
    from models.db.project_entity import ProjectEntity  # noqa: F401
    from models.db.learning_path_entity import LearningPathEntity  # noqa: F401
    from models.db.category_entity import CategoryEntity  # noqa: F401
    from models.db.question_entity import QuestionEntity  # noqa: F401
    from models.db.answer_entity import AnswerEntity  # noqa: F401
    from models.db.insight_entity import InsightEntity  # noqa: F401
    from models.db.project_step_entity import ProjectStepEntity  # noqa: F401

    Base.metadata.create_all(bind=engine)