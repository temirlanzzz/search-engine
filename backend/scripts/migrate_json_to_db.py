#!/usr/bin/env python3
"""
Migration script to move from JSON file storage to PostgreSQL database
"""

import os
import json
import sys
from pathlib import Path

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db, SessionLocal
from app.services.document_service import DocumentService
from app.services.index_service import IndexService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate_documents():
    """Migrate documents from JSON files to database"""
    logger.info("Starting document migration...")
    
    # Paths
    base_dir = Path(__file__).parent.parent.parent
    docs_dir = base_dir / "data" / "docs"
    tokens_dir = base_dir / "data" / "tokens"
    
    if not docs_dir.exists():
        logger.warning(f"Documents directory not found: {docs_dir}")
        return
    
    db = SessionLocal()
    try:
        doc_service = DocumentService(db)
        
        # Count existing documents
        existing_count = doc_service.get_document_count()
        logger.info(f"Found {existing_count} existing documents in database")
        
        # Migrate documents
        migrated_count = 0
        for doc_file in docs_dir.glob("*.json"):
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    doc_data = json.load(f)
                
                # Create document in database
                document = doc_service.create_document(
                    url=doc_data.get('url', ''),
                    title=doc_data.get('title', ''),
                    content=doc_data.get('content', ''),
                    html_content=doc_data.get('html_content', '')
                )
                
                migrated_count += 1
                logger.info(f"Migrated document: {doc_data.get('title', 'Unknown')}")
                
            except Exception as e:
                logger.error(f"Error migrating document {doc_file}: {e}")
        
        logger.info(f"Document migration completed. Migrated {migrated_count} documents.")
        
    finally:
        db.close()


def migrate_search_index():
    """Migrate search index from JSON files to database"""
    logger.info("Starting search index migration...")
    
    # Paths
    base_dir = Path(__file__).parent.parent.parent
    tfidf_file = base_dir / "index" / "tfidf_index.json"
    inverted_file = base_dir / "index" / "inverted_index.json"
    
    if not tfidf_file.exists():
        logger.warning(f"TF-IDF index file not found: {tfidf_file}")
        return
    
    db = SessionLocal()
    try:
        index_service = IndexService(db)
        
        # Rebuild index from database (this will be more accurate)
        logger.info("Rebuilding search index from database...")
        result = index_service.rebuild_index()
        
        if result.get('status') == 'success':
            logger.info(f"Search index rebuilt successfully. Indexed {result.get('terms_indexed', 0)} terms.")
        else:
            logger.error(f"Failed to rebuild search index: {result.get('error', 'Unknown error')}")
        
    finally:
        db.close()


def main():
    """Main migration function"""
    logger.info("Starting JSON to PostgreSQL migration...")
    
    try:
        # Initialize database
        init_db()
        logger.info("Database initialized")
        
        # Migrate documents
        migrate_documents()
        
        # Migrate search index
        migrate_search_index()
        
        logger.info("Migration completed successfully!")
        
        # Print summary
        db = SessionLocal()
        try:
            doc_service = DocumentService(db)
            index_service = IndexService(db)
            
            doc_count = doc_service.get_document_count()
            stats = index_service.get_index_stats()
            
            print("\n" + "="*50)
            print("MIGRATION SUMMARY")
            print("="*50)
            print(f"Documents in database: {doc_count}")
            print(f"Terms in search index: {stats.get('total_terms', 0)}")
            print(f"Top terms: {[term['term'] for term in stats.get('top_terms', [])[:5]]}")
            print("="*50)
            
        finally:
            db.close()
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 