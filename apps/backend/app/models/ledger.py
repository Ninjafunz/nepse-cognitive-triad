"""T+2 Settlement Aware Account Ledger."""

import uuid
from datetime import datetime, date
from sqlalchemy import String, Float, DateTime, Date, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class AccountLedger(Base):
    __tablename__ = "account_ledger"
    __table_args__ = (
        Index("ix_ledger_settled_date", "settled_date"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entry_type: Mapped[str] = mapped_column(String(50), nullable=False)  # deposit, withdrawal, buy, sell, fee, settlement
    amount: Mapped[float] = mapped_column(Float, nullable=False)  # Positive for credit, negative for debit
    currency: Mapped[str] = mapped_column(String(10), default="NPR")
    trade_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    settled_date: Mapped[date] = mapped_column(Date, nullable=False)  # Effective cash date (T+2)
    order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
