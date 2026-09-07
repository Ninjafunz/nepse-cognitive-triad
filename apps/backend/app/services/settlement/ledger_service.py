"""Ledger service for calculating real-time settled cash and buying power."""

from datetime import date
from typing import Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ledger import AccountLedger
from app.models.positions import Position
from app.config import settings


class LedgerService:
    """Manages virtual funds, ledger entries, and available buying power with T+2 constraints."""

    async def initialize_account_balance(self, session: AsyncSession):
        """Seeds initial virtual deposit if ledger is empty."""
        stmt = select(func.count(AccountLedger.id))
        count = await session.scalar(stmt)
        if count == 0:
            today = date.today()
            initial_deposit = AccountLedger(
                entry_type="deposit",
                amount=settings.INITIAL_VIRTUAL_CAPITAL_NPR,
                currency="NPR",
                trade_date=today,
                settled_date=today,  # Initial capital is immediately settled
                description=f"Initial Virtual Capital Injection ($100k USD equivalent)",
            )
            session.add(initial_deposit)
            await session.commit()

    async def get_portfolio_summary(self, session: AsyncSession) -> Dict[str, Any]:
        """Calculates settled cash, unsettled cash, equity, and available buying power."""
        today = date.today()

        # Settled Cash (Entries where settled_date <= today)
        settled_stmt = select(func.coalesce(func.sum(AccountLedger.amount), 0.0)).where(
            AccountLedger.settled_date <= today
        )
        settled_cash = float(await session.scalar(settled_stmt))

        # Unsettled Cash (Entries where settled_date > today)
        unsettled_stmt = select(func.coalesce(func.sum(AccountLedger.amount), 0.0)).where(
            AccountLedger.settled_date > today
        )
        unsettled_cash = float(await session.scalar(unsettled_stmt))

        # Unrealized and Realized PnL from open positions
        pos_stmt = select(
            func.coalesce(func.sum(Position.quantity * Position.current_price), 0.0),
            func.coalesce(func.sum(Position.unrealized_pnl), 0.0),
            func.coalesce(func.sum(Position.realized_pnl), 0.0),
        )
        pos_res = await session.execute(pos_stmt)
        holdings_market_val, total_unrealized_pnl, total_realized_pnl = pos_res.one()

        total_equity = settled_cash + unsettled_cash + float(holdings_market_val)

        return {
            "total_equity_npr": total_equity,
            "settled_cash_npr": settled_cash,
            "unsettled_cash_npr": unsettled_cash,
            "available_buying_power_npr": max(0.0, settled_cash),  # Unsettled funds cannot be used to buy
            "unrealized_pnl_npr": float(total_unrealized_pnl),
            "realized_pnl_npr": float(total_realized_pnl),
            "currency": "NPR",
        }


ledger_service = LedgerService()
