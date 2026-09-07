"""Order execution and history Pydantic schemas."""

import uuid
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field


class OrderCreateRequest(BaseModel):
    symbol: str = Field(..., max_length=20, examples=["NABIL"])
    side: Literal["BUY", "SELL"]
    order_type: Literal["MARKET", "LIMIT"] = "MARKET"
    quantity: int = Field(..., gt=0, description="Number of shares (must be > 0)")
    limit_price: Optional[float] = Field(None, gt=0, description="Required if LIMIT order")


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    symbol: str
    side: str
    order_type: str
    quantity: int
    limit_price: Optional[float] = None
    filled_qty: int
    avg_fill_price: float
    broker_commission: float
    sebon_fee: float
    dp_charge: float
    total_cost: float
    status: str
    rejection_reason: Optional[str] = None
    ai_confidence: Optional[float] = None
    created_at: datetime
