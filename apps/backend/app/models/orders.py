"""Virtual Orders table model."""

import uuid
from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("side IN ('BUY', 'SELL')", name="check_valid_order_side_no_short"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol: Mapped[str] = mapped_column(String(20), ForeignKey("securities.symbol", ondelete="CASCADE"), index=True)
    side: Mapped[str] = mapped_column(String(10), nullable=False)  # BUY or SELL only (NEPSE does not allow shorting)
    order_type: Mapped[str] = mapped_column(String(20), default="MARKET")  # MARKET, LIMIT
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_price: Mapped[float] = mapped_column(Float, nullable=True)
    filled_qty: Mapped[int] = mapped_column(Integer, default=0)
    avg_fill_price: Mapped[float] = mapped_column(Float, default=0.0)
    broker_commission: Mapped[float] = mapped_column(Float, default=0.0)
    sebon_fee: Mapped[float] = mapped_column(Float, default=0.0)
    dp_charge: Mapped[float] = mapped_column(Float, default=0.0)
    total_cost: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(30), default="PENDING", index=True)  # PENDING, FILLED, REJECTED, CANCELLED
    rejection_reason: Mapped[str] = mapped_column(String(255), nullable=True)
    ai_confidence: Mapped[float] = mapped_column(Float, nullable=True)
    triad_decision_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
