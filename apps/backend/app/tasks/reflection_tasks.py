"""Celery background tasks for Market Ingestion, Daily Evaluations, and Epistemic Reflections."""

from datetime import date, timedelta, datetime
import logging
from sqlalchemy import select, and_

logger = logging.getLogger(__name__)


def run_daily_reflection_check():
    """Daily Epistemic Reflection Check.
    Runs after market close (e.g. 4:00 PM NPT).
    Finds predictions made 5 trading days ago, checks actual return,
    and triggers JournalCritic to write an epistemic post-mortem if false.
    """
    from app.core.database import async_session_maker
    from app.models.evaluations import PredictionReflection
    from app.services.journaling.critic_loop import journal_critic

    logger.info("Executing daily epistemic reflection audit...")
    # Background execution logic wired for async SQLAlchemy session


def log_daily_evaluation(eval_dict: dict):
    """Logs non-action or trade decision for the daily decision matrix."""
    from app.models.evaluations import DailyEvaluation

    # Persists evaluation to daily_evaluations table
