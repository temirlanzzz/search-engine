from celery import Celery
from app.crawler.crawler import SimpleCrawler
from app.services.index_service import IndexService
from app.database import SessionLocal
import os

# Get configuration from environment
broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
backend_url = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

celery_app = Celery(
    "search_engine",
    broker=broker_url,
    backend=backend_url
)

@celery_app.task(name="rebuild_index_task")
def rebuild_index_task():
    db = SessionLocal()
    try:
        index_service = IndexService(db)
        result = index_service.rebuild_index()
        return result
    finally:
        db.close()

@celery_app.task(name="crawl_and_index_task")
def crawl_and_index_task(urls):
    try:
        # Crawl and store documents to database
        crawler = SimpleCrawler(urls, max_pages=20, delay=1)
        crawler.crawl_and_store()
        
        # Rebuild index
        db = SessionLocal()
        try:
            index_service = IndexService(db)
            result = index_service.rebuild_index()
            return result
        finally:
            db.close()
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
