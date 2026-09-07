"""Celery Application initialization and task schedule configuration."""

from celery import Celery
from app.config import settings

celery_app = Celery(
    "nepse_triad_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.market_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kathmandu",
    enable_utc=True,
    task_track_started=True,
    # Periodic schedules via Celery Beat
    beat_schedule={
        "poll-nepse-live-data-during-market": {
            "task": "app.tasks.market_tasks.poll_nepse_live_data",
            "schedule": 5.0,  # every 5 seconds
        },
        "settle-t2-transactions-daily": {
            "task": "app.tasks.market_tasks.run_daily_settlement",
            "schedule": 3600.0,  # checked hourly
        },
    },
)
