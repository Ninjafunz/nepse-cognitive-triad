"""Portfolio and Ledger Pydantic schemas."""

import uuid
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class PositionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    symbol: str
    quantity: int
    avg_cost: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float
    last_updated: datetime


class PortfolioBalanceResponse(BaseModel):
    total_equity_npr: float
    unrealized_pnl_npr: float
    realized_pnl_npr: float
    settled_cash_npr: float
    unsettled_cash_npr: float
    available_buying_power_npr: float
    currency: str = "NPR"


class LedgerEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    entry_type: str
    amount: float
    currency: str
    trade_date: date
    settled_date: date
    description: Optional[str] = None
    created_at: datetime
