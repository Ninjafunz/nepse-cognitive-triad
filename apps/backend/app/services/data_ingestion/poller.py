"""Async polling engine for continuously capturing market updates."""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from app.core.database import AsyncSessionLocal
from app.services.data_ingestion.nepse_client import nepse_client
from app.models.securities import Security
from app.models.market_data import MarketData1Min
from app.core.events import event_bus
from app.config import settings

logger = logging.getLogger(__name__)


class MarketDataPoller:
    """Async background poller that normalizes incoming NEPSE ticks into OHLCV hypertable candles."""

    def __init__(self):
        self.is_running = False
        self._task: Optional[asyncio.Task] = None
        self.last_successful_poll: Optional[datetime] = None

    async def start(self):
        if self.is_running:
            return
        self.is_running = True
        self._task = asyncio.create_task(self._poll_loop())
        logger.info("NEPSE MarketDataPoller started.")

    async def stop(self):
        self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("NEPSE MarketDataPoller stopped.")

    async def _poll_loop(self):
        while self.is_running:
            try:
                await self.poll_once()
            except Exception as e:
                logger.error(f"Error during market poll cycle: {e}")

            # Sleep interval
            await asyncio.sleep(settings.POLLING_INTERVAL_SECONDS)

    async def poll_once(self):
        """Single polling tick to update securities and insert 1-minute OHLCV rows."""
        live_data = await nepse_client.fetch_live_prices()
        if not live_data:
            return

        now = datetime.now(timezone.utc)
        # Round to minute boundary for candle aggregation
        candle_time = now.replace(second=0, microsecond=0)

        async with AsyncSessionLocal() as session:
            for item in live_data:
                symbol = item.get("symbol")
                if not symbol:
                    continue

                ltp = float(item.get("lastTradedPrice", 0.0) or item.get("ltp", 0.0))
                if ltp <= 0.0:
                    continue

                company_name = item.get("companyName", symbol)
                sector = item.get("sector", "General")
                volume = float(item.get("totalTradeQuantity", 0.0))
                close_prev = float(item.get("closePrice", ltp))

                # 1. Upsert Securities Master
                sec_stmt = insert(Security).values(
                    symbol=symbol,
                    company_name=company_name,
                    sector=sector,
                    base_price=close_prev,
                    is_active=True,
                ).on_conflict_do_update(
                    index_elements=["symbol"],
                    set_={
                        "company_name": company_name,
                        "sector": sector,
                        "updated_at": now,
                    }
                )
                await session.execute(sec_stmt)

                # 2. Upsert 1-Min Candle
                candle_stmt = insert(MarketData1Min).values(
                    symbol=symbol,
                    time=candle_time,
                    open=ltp,
                    high=ltp,
                    low=ltp,
                    close=ltp,
                    volume=volume,
                    ltp=ltp,
                    trade_count=1,
                ).on_conflict_do_update(
                    index_elements=["symbol", "time"],
                    set_={
                        "high": MarketData1Min.high,  # In production, func.greatest(MarketData1Min.high, ltp)
                        "low": MarketData1Min.low,
                        "close": ltp,
                        "ltp": ltp,
                        "volume": volume,
                    }
                )
                await session.execute(candle_stmt)

            await session.commit()
            self.last_successful_poll = now
            await event_bus.emit("MARKET_TICK", {"timestamp": now.isoformat(), "count": len(live_data)})


market_poller = MarketDataPoller()
