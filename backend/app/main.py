from fastapi import FastAPI, Query, Body, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db, check_db_connection
from app.services.document_service import DocumentService, get_document_service
from app.services.index_service import IndexService, get_index_service
from app.search.redis_search import search_redis_query
from tasks import rebuild_index_task, crawl_and_index_task
from scripts.run_crawler import crawl_and_store
import redis
from celery.result import AsyncResult
from tasks import celery_app
import logging

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

app = FastAPI(title="Search Engine API", version="0.1")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Search Engine API...")
    
    # Initialize database
    try:
        init_db()
        if not check_db_connection():
            logger.error("Database connection failed")
            raise Exception("Database connection failed")
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

@app.get("/")
def read_root():
    return {"message": "Search Engine Backend is running"}

@app.get("/search")
def search_query(
    q: str = Query(...), 
    op: str = Query("AND"),
    index_service: IndexService = Depends(get_index_service)
):
    try:
        logger.info(f"Searching for: '{q}' with operation: {op}")
        results = index_service.search(q, op)
        logger.info(f"Found {len(results)} results for query: '{q}'")
        return {"results": results, "count": len(results)}
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail="Search failed")

@app.get("/search_redis")
def search_redis(q: str = Query(...), op: str = Query("AND")):
    results = search_redis_query(q, op)
    return {"query": q, "results": results}

@app.post("/rebuild-index")
def trigger_index_rebuild(index_service: IndexService = Depends(get_index_service)):
    try:
        result = index_service.rebuild_index()
        return result
    except Exception as e:
        logger.error(f"Index rebuild error: {e}")
        raise HTTPException(status_code=500, detail="Index rebuild failed")

@app.post("/crawl")
def run_crawler(
    urls: list[str] = Body(...),
    document_service: DocumentService = Depends(get_document_service),
    index_service: IndexService = Depends(get_index_service)
):
    try:
        # Crawl and store documents
        crawl_and_store(urls)
        
        # Rebuild index
        result = index_service.rebuild_index()
        
        return {
            "status": "Crawled and index rebuilt",
            "index_result": result
        }
    except Exception as e:
        logger.error(f"Crawl error: {e}")
        raise HTTPException(status_code=500, detail="Crawl failed")

@app.post("/task/rebuild")
def trigger_rebuild():
    task = rebuild_index_task.delay()
    return {"task_id": task.id}

@app.post("/task/crawl")
def trigger_crawl(urls: list[str] = Body(...)):
    task = crawl_and_index_task.delay(urls)
    return {"task_id": task.id}

@app.get("/task/status/{task_id}")
def get_task_status(task_id: str):
    r = redis.Redis(db=1)
    status = r.hget(f"celery-task-meta-{task_id}", "status")
    return {"task_id": task_id, "status": status.decode() if status else "UNKNOWN"}

@app.get("/task/status/async/{task_id}")
def get_async_task_status(task_id: str):
    task = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task.id,
        "status": task.status,
        "result": task.result if task.ready() else None
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        db_ok = check_db_connection()
        redis_ok = True
        try:
            r = redis.Redis.from_url(settings.redis_url)
            r.ping()
        except:
            redis_ok = False
        
        return {
            "status": "healthy" if db_ok and redis_ok else "unhealthy",
            "database": "connected" if db_ok else "disconnected",
            "redis": "connected" if redis_ok else "disconnected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.get("/stats")
def get_stats(index_service: IndexService = Depends(get_index_service)):
    """Get search engine statistics"""
    try:
        stats = index_service.get_index_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")

@app.get("/suggestions")
def get_suggestions(
    q: str = Query(...),
    index_service: IndexService = Depends(get_index_service)
):
    """Get search suggestions based on indexed terms"""
    try:
        suggestions = index_service.get_search_suggestions(q)
        return {"suggestions": suggestions}
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        raise HTTPException(status_code=500, detail="Failed to get suggestions")

@app.get("/crawl-stats")
def get_crawl_stats(index_service: IndexService = Depends(get_index_service)):
    """Get crawling statistics"""
    try:
        stats = index_service.get_crawl_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting crawl stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get crawl statistics")

@app.get("/debug/index")
def debug_index(index_service: IndexService = Depends(get_index_service)):
    """Debug endpoint to check index status"""
    try:
        from app.database import SearchIndex, Document
        db = next(get_db())
        
        total_docs = db.query(Document).count()
        total_terms = db.query(SearchIndex).count()
        
        # Get a few sample terms
        sample_terms = db.query(SearchIndex).limit(5).all()
        
        return {
            "total_documents": total_docs,
            "total_indexed_terms": total_terms,
            "sample_terms": [term.term for term in sample_terms],
            "index_built": total_terms > 0
        }
    except Exception as e:
        logger.error(f"Error in debug endpoint: {e}")
        return {"error": str(e)}

@app.get("/tasks/active")
def get_active_tasks():
    """Get active tasks from Celery"""
    try:
        # Get active tasks from Celery
        active_tasks = celery_app.control.inspect().active()
        if not active_tasks:
            return {"tasks": []}
        
        # Format tasks for frontend
        formatted_tasks = []
        for worker, tasks in active_tasks.items():
            for task in tasks:
                formatted_tasks.append({
                    "id": task["id"],
                    "type": task["name"],
                    "status": "PROGRESS",
                    "created_at": task.get("time_start", ""),
                    "result": None
                })
        
        return {"tasks": formatted_tasks}
    except Exception as e:
        logger.error(f"Error getting active tasks: {e}")
        return {"tasks": []}
