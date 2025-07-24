from sqlalchemy.orm import Session
from app.database import Document, Token, get_db
from app.utilts.tokenizer import tokenize_text
import json
import hashlib
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_document(self, url: str, title: str, content: str, html_content: str = None) -> Document:
        """Create a new document in the database"""
        try:
            # Generate document ID from URL
            doc_id = hashlib.md5(url.encode()).hexdigest()
            
            # Check if document already exists
            existing_doc = self.db.query(Document).filter(Document.id == doc_id).first()
            if existing_doc:
                # Update existing document
                existing_doc.title = title
                existing_doc.content = content
                existing_doc.html_content = html_content
                self.db.commit()
                logger.info(f"Updated existing document: {url}")
                return existing_doc
            
            # Create new document
            document = Document(
                id=doc_id,
                url=url,
                title=title,
                content=content,
                html_content=html_content
            )
            self.db.add(document)
            self.db.commit()
            self.db.refresh(document)
            
            # Tokenize and store tokens
            self._store_tokens(doc_id, content)
            
            logger.info(f"Created new document: {url}")
            return document
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating document {url}: {e}")
            raise
    
    def _store_tokens(self, doc_id: str, content: str):
        """Store tokenized content in the database"""
        try:
            # Remove existing tokens for this document
            self.db.query(Token).filter(Token.document_id == doc_id).delete()
            
            # Tokenize content
            tokens = tokenize_text(content)
            
            # Store tokens with positions
            token_records = []
            token_freq = {}
            
            for position, token in enumerate(tokens):
                token_freq[token] = token_freq.get(token, 0) + 1
                token_records.append(Token(
                    document_id=doc_id,
                    token=token,
                    position=position,
                    frequency=token_freq[token]
                ))
            
            self.db.add_all(token_records)
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error storing tokens for document {doc_id}: {e}")
            raise
    
    def get_document(self, doc_id: str) -> Optional[Document]:
        """Get document by ID"""
        return self.db.query(Document).filter(Document.id == doc_id).first()
    
    def get_document_by_url(self, url: str) -> Optional[Document]:
        """Get document by URL"""
        return self.db.query(Document).filter(Document.url == url).first()
    
    def get_all_documents(self, limit: int = 100, offset: int = 0) -> List[Document]:
        """Get all documents with pagination"""
        return self.db.query(Document).offset(offset).limit(limit).all()
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete document and its tokens"""
        try:
            # Delete tokens first
            self.db.query(Token).filter(Token.document_id == doc_id).delete()
            
            # Delete document
            document = self.db.query(Document).filter(Document.id == doc_id).first()
            if document:
                self.db.delete(document)
                self.db.commit()
                logger.info(f"Deleted document: {doc_id}")
                return True
            return False
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting document {doc_id}: {e}")
            raise
    
    def get_document_count(self) -> int:
        """Get total number of documents"""
        return self.db.query(Document).count()
    
    def search_documents_by_tokens(self, tokens: List[str]) -> List[Document]:
        """Search documents containing specific tokens"""
        from sqlalchemy import and_
        
        # Find documents that contain all tokens
        query = self.db.query(Document).join(Token, Document.id == Token.document_id)
        
        for token in tokens:
            query = query.filter(Token.token == token)
        
        return query.distinct().all()
    
    def get_document_tokens(self, doc_id: str) -> List[str]:
        """Get all tokens for a document"""
        tokens = self.db.query(Token).filter(
            Token.document_id == doc_id
        ).order_by(Token.position).all()
        return [token.token for token in tokens]


def get_document_service():
    """Dependency to get document service"""
    db = next(get_db())
    return DocumentService(db) 