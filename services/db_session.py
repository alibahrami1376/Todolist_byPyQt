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