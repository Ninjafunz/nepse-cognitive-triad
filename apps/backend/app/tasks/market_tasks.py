"""Periodic Celery background tasks for NEPSE polling and daily settlement."""

import asyncio
from app.core.celery_app import celery_app
from app.services.data_ingestion.poller import market_poller
from app.services.data_ingestion.nepse_client import nepse_client
from app.core.database import AsyncSessionLocal
from app.services.settlement.ledger_service import ledger_service


@celery_app.task(name="app.tasks.market_tasks.poll_nepse_live_data")
def poll_nepse_live_data():
    """Runs single tick of live market polling if market is open."""
    if nepse_client.is_market_open():
        asyncio.run(market_poller.poll_once())
        return "Market Polled"
    return "Market Closed"


@celery_app.task(name="app.tasks.market_tasks.run_daily_settlement")
def run_daily_settlement():
    """Daily routine verifying ledger state."""
    async def _init():
        async with AsyncSessionLocal() as session:
            await ledger_service.initialize_account_balance(session)

    asyncio.run(_init())
    return "Settlement ledger synchronized"
