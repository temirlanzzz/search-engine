from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Index, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from app.config import settings
import logging

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

# Database setup
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String(255), primary_key=True)
    url = Column(String(2048), nullable=False)
    title = Column(String(500), nullable=True)
    content = Column(Text, nullable=True)
    html_content = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Index for faster searches
    __table_args__ = (
        Index('idx_documents_url', 'url'),
        Index('idx_documents_title', 'title'),
    )


class Token(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True)
    document_id = Column(String(255), nullable=False)
    token = Column(String(255), nullable=False)
    position = Column(Integer, nullable=False)
    frequency = Column(Integer, default=1)
    
    # Indexes for faster searches
    __table_args__ = (
        Index('idx_tokens_document_id', 'document_id'),
        Index('idx_tokens_token', 'token'),
        Index('idx_tokens_document_token', 'document_id', 'token'),
    )


class SearchIndex(Base):
    __tablename__ = "search_indices"
    
    id = Column(Integer, primary_key=True)
    term = Column(String(255), nullable=False, unique=True)
    document_frequency = Column(Integer, default=0)
    tfidf_data = Column(Text, nullable=True)  # JSON string of doc_id -> tfidf_score
    inverted_index_data = Column(Text, nullable=True)  # JSON string of doc_ids list
    
    # Index for faster searches
    __table_args__ = (
        Index('idx_search_indices_term', 'term'),
    )


class CrawlTask(Base):
    __tablename__ = "crawl_tasks"
    
    id = Column(String(255), primary_key=True)
    urls = Column(Text, nullable=False)  # JSON array of URLs
    status = Column(String(50), default="PENDING")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def check_db_connection():
    """Check if database connection is working"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False 