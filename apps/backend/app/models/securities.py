"""Securities Master table model."""

from datetime import datetime
from sqlalchemy import String, Boolean, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class Security(Base):
    __tablename__ = "securities"

    symbol: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sector: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    instrument_type: Mapped[str] = mapped_column(String(50), default="Equity")
    base_price: Mapped[float] = mapped_column(Float, nullable=True)
    listing_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
