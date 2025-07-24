# backend/celery_worker.py

from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",  # store task results
)

celery_app.conf.task_track_started = True
