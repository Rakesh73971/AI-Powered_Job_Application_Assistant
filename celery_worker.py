from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "ai_job_assistant",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.analysis_task"]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

if __name__ == "__main__":
    celery_app.start()
