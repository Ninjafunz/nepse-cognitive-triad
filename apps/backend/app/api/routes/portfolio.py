"""Portfolio and Virtual Ledger API endpoints."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.api.deps import get_db
from app.models.positions import Position
from app.models.ledger import AccountLedger
from app.schemas.portfolio import PositionResponse, PortfolioBalanceResponse, LedgerEntryResponse
from app.services.settlement.ledger_service import ledger_service

router = APIRouter()


@router.get("/balance", response_model=PortfolioBalanceResponse)
async def get_portfolio_balance(db: AsyncSession = Depends(get_db)):
    """Returns real-time settled cash, unsettled T+2 funds, and available buying power."""
    await ledger_service.initialize_account_balance(db)
    return await ledger_service.get_portfolio_summary(db)


@router.get("/positions", response_model=List[PositionResponse])
async def list_positions(db: AsyncSession = Depends(get_db)):
    """Returns currently held virtual stock positions with unrealized PnL."""
    stmt = select(Position).where(Position.quantity > 0)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.get("/ledger", response_model=List[LedgerEntryResponse])
async def list_ledger_entries(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """Returns the immutable audit log of transactions and T+2 settlement dates."""
    stmt = select(AccountLedger).order_by(desc(AccountLedger.created_at)).limit(limit)
    res = await db.execute(stmt)
    return res.scalars().all()
