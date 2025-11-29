from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, update, delete
from services.db_session import get_session, Base, engine
from models.db.document_entity import DocumentEntity, DocumentBlockEntity


class DocumentService:
    def __init__(self):
        # جداول به صورت خودکار در init_db ایجاد می‌شوند
        pass

    def create_document(
        self,
        title: str,
        course_id: Optional[str] = None,
        textbook_id: Optional[str] = None
    ) -> str:
        """ایجاد سند جدید"""
        with get_session() as db:
            document = DocumentEntity(
                title=title,
                course_id=course_id,
                textbook_id=textbook_id
            )
            db.add(document)
            db.commit()
            db.refresh(document)
            return document.id

    def get_all_documents(
        self, 
        course_id: Optional[str] = None,
        textbook_id: Optional[str] = None
    ) -> List[DocumentEntity]:
        """دریافت همه سندها"""
        with get_session() as db:
            stmt = select(DocumentEntity)
            if course_id:
                stmt = stmt.where(DocumentEntity.course_id == course_id)
            if textbook_id:
                stmt = stmt.where(DocumentEntity.textbook_id == textbook_id)
            stmt = stmt.order_by(DocumentEntity.updated_at.desc())
            result = db.execute(stmt)
            documents = list(result.scalars().all())
            for doc in documents:
                db.expunge(doc)
            return documents

    def get_document_by_id(self, document_id: str) -> Optional[DocumentEntity]:
        """دریافت سند بر اساس ID"""
        with get_session() as db:
            stmt = select(DocumentEntity).where(DocumentEntity.id == document_id)
            result = db.execute(stmt)
            doc = result.scalar_one_or_none()
            if doc:
                db.expunge(doc)
            return doc

    def update_document(
        self,
        document_id: str,
        title: Optional[str] = None,
        course_id: Optional[str] = None,
        textbook_id: Optional[str] = None
    ) -> bool:
        """به‌روزرسانی سند"""
        with get_session() as db:
            document = db.execute(
                select(DocumentEntity).where(DocumentEntity.id == document_id)
            ).scalar_one_or_none()
            
            if not document:
                return False
            
            if title is not None:
                document.title = title
            if course_id is not None:
                document.course_id = course_id
            if textbook_id is not None:
                document.textbook_id = textbook_id
            
            document.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(document)
            return True

    def delete_document(self, document_id: str) -> bool:
        """حذف سند"""
        with get_session() as db:
            stmt = delete(DocumentEntity).where(DocumentEntity.id == document_id)
            result = db.execute(stmt)
            db.commit()
            return result.rowcount > 0

    def get_document_blocks(self, document_id: str) -> List[DocumentBlockEntity]:
        """دریافت بلوک‌های یک سند"""
        with get_session() as db:
            stmt = select(DocumentBlockEntity).where(
                DocumentBlockEntity.document_id == document_id
            ).order_by(DocumentBlockEntity.order_index.asc())
            result = db.execute(stmt)
            blocks = list(result.scalars().all())
            for block in blocks:
                db.expunge(block)
            return blocks

    def get_block_by_id(self, block_id: str) -> Optional[DocumentBlockEntity]:
        """دریافت بلوک بر اساس ID"""
        with get_session() as db:
            stmt = select(DocumentBlockEntity).where(DocumentBlockEntity.id == block_id)
            result = db.execute(stmt)
            block = result.scalar_one_or_none()
            if block:
                db.expunge(block)
            return block

    def create_block(
        self,
        document_id: str,
        block_type: str,
        content: Optional[str] = None,
        order_index: int = 0,
        block_metadata: Optional[str] = None
    ) -> str:
        """ایجاد بلوک جدید"""
        with get_session() as db:
            block = DocumentBlockEntity(
                document_id=document_id,
                block_type=block_type,
                content=content,
                order_index=order_index,
                block_metadata=block_metadata
            )
            db.add(block)
            db.commit()
            db.refresh(block)
            return block.id

    def update_block(
        self,
        block_id: str,
        block_type: Optional[str] = None,
        content: Optional[str] = None,
        order_index: Optional[int] = None,
        block_metadata: Optional[str] = None
    ) -> bool:
        """به‌روزرسانی بلوک"""
        with get_session() as db:
            block = db.execute(
                select(DocumentBlockEntity).where(DocumentBlockEntity.id == block_id)
            ).scalar_one_or_none()
            
            if not block:
                return False
            
            if block_type is not None:
                block.block_type = block_type
            if content is not None:
                block.content = content
            if order_index is not None:
                block.order_index = order_index
            if block_metadata is not None:
                block.block_metadata = block_metadata
            
            block.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(block)
            return True

    def delete_block(self, block_id: str) -> bool:
        """حذف بلوک"""
        with get_session() as db:
            stmt = delete(DocumentBlockEntity).where(DocumentBlockEntity.id == block_id)
            result = db.execute(stmt)
            db.commit()
            return result.rowcount > 0

    def reorder_blocks(self, document_id: str, block_orders: dict[str, int]) -> bool:
        """تغییر ترتیب بلوک‌ها"""
        with get_session() as db:
            for block_id, order_index in block_orders.items():
                stmt = update(DocumentBlockEntity).where(
                    DocumentBlockEntity.id == block_id,
                    DocumentBlockEntity.document_id == document_id
                ).values(order_index=order_index)
                db.execute(stmt)
            db.commit()
            return True
