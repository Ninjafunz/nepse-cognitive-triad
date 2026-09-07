"""Trade Journals and Post-Trade Reflections table models."""

import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class TradeJournal(Base):
    __tablename__ = "trade_journals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    triad_decision_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("triad_decisions.id", ondelete="CASCADE"), index=True)
    journal_type: Mapped[str] = mapped_column(String(30), default="pre_trade")  # pre_trade, post_trade_reflection
    thesis_summary: Mapped[str] = mapped_column(String(500), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    citations: Mapped[list] = mapped_column(JSONB, default=list)  # Author, book, excerpt references
    model_used: Mapped[str] = mapped_column(String(50), default="llama3:70b")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class PostTradeReflection(Base):
    __tablename__ = "post_trade_reflections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    original_thesis: Mapped[str] = mapped_column(Text, nullable=False)
    actual_outcome: Mapped[str] = mapped_column(Text, nullable=False)
    reflection_content: Mapped[str] = mapped_column(Text, nullable=False)
    route_accuracy: Mapped[dict] = mapped_column(JSONB, default=dict)  # {"alpha": true, "beta": false, "gamma": true}
    lesson_learned: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
