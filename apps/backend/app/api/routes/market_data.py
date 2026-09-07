"""Market Data API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.api.deps import get_db
from app.models.securities import Security
from app.models.market_data import MarketData1Min
from app.schemas.market_data import SecurityResponse, MarketStatusResponse, CandleResponse
from app.services.data_ingestion.nepse_client import nepse_client

router = APIRouter()


@router.get("/status", response_model=MarketStatusResponse)
async def get_market_status():
    """Returns whether NEPSE is currently open along with turnover/index metadata."""
    return await nepse_client.fetch_market_status()


@router.get("/securities", response_model=List[SecurityResponse])
async def list_securities(
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    """Lists registered NEPSE securities and current reference prices."""
    stmt = select(Security).where(Security.is_active == True).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/candles/{symbol}", response_model=List[CandleResponse])
async def get_candles(
    symbol: str,
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """Retrieves 1-minute OHLCV candles for charting."""
    stmt = (
        select(MarketData1Min)
        .where(MarketData1Min.symbol == symbol.upper())
        .order_by(desc(MarketData1Min.time))
        .limit(limit)
    )
    result = await db.execute(stmt)
    candles = result.scalars().all()
    return list(reversed(candles))
