"""TimescaleDB 1-minute OHLCV hypertable model."""

from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime, PrimaryKeyConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class MarketData1Min(Base):
    __tablename__ = "market_data_1min"
    __table_args__ = (
        PrimaryKeyConstraint("symbol", "time"),
        Index("ix_market_data_symbol_time_desc", "symbol", "time"),
    )

    symbol: Mapped[str] = mapped_column(String(20), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float] = mapped_column(Float, default=0.0)
    ltp: Mapped[float] = mapped_column(Float, nullable=False)
    trade_count: Mapped[int] = mapped_column(Integer, default=0)
