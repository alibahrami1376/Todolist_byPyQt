import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from services.db_session import Base


class DocumentEntity(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default=lambda: str(uuid.uuid4().hex))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    course_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("courses.id"), nullable=True)
    textbook_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("textbooks.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    
    # Relationships
    course: Mapped[Optional["CourseEntity"]] = relationship(back_populates="documents")
    textbook: Mapped[Optional["TextbookEntity"]] = relationship(back_populates="documents")
    blocks: Mapped[list["DocumentBlockEntity"]] = relationship(
        back_populates="document", 
        cascade="all, delete-orphan",
        order_by="DocumentBlockEntity.order_index"
    )


class DocumentBlockEntity(Base):
    __tablename__ = "document_blocks"

    id: Mapped[str] = mapped_column(String(50), primary_key=True, default=lambda: str(uuid.uuid4().hex))
    document_id: Mapped[str] = mapped_column(String(50), ForeignKey("documents.id"), nullable=False)
    block_type: Mapped[str] = mapped_column(String(50), nullable=False)  # text, heading1, heading2, heading3, code, image, list
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # برای ترتیب نمایش
    block_metadata: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON برای اطلاعات اضافی (مثلاً URL عکس)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    
    # Relationships
    document: Mapped["DocumentEntity"] = relationship(back_populates="blocks")

