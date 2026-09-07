"""Corporate Actions table model (Dividends, Right Shares, Splits)."""

import uuid
from datetime import datetime, date
from sqlalchemy import String, Float, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class CorporateAction(Base):
    __tablename__ = "corporate_actions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol: Mapped[str] = mapped_column(String(20), ForeignKey("securities.symbol", ondelete="CASCADE"), index=True)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)  # dividend, bonus, right, split
    value: Mapped[float] = mapped_column(Float, nullable=False)  # percentage or ratio
    announcement_date: Mapped[date] = mapped_column(Date, nullable=True)
    book_close_date: Mapped[date] = mapped_column(Date, nullable=True, index=True)
    record_date: Mapped[date] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
