"""Market Data Pydantic schemas."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class SecurityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    company_name: str
    sector: str
    instrument_type: str
    base_price: Optional[float] = None
    is_active: bool


class MarketStatusResponse(BaseModel):
    is_open: bool
    current_time_npt: str
    market_index: Optional[float] = None
    index_change: Optional[float] = None
    percent_change: Optional[float] = None
    turnover_npr: Optional[float] = None


class CandleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    ltp: float
    trade_count: int


class TopMoverItem(BaseModel):
    symbol: str
    ltp: float
    point_change: float
    percent_change: float
