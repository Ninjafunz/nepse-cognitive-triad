"""Cognitive Triad decisions and consensus records table model."""

import uuid
from datetime import datetime
from sqlalchemy import String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class TriadDecision(Base):
    __tablename__ = "triad_decisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol: Mapped[str] = mapped_column(String(20), ForeignKey("securities.symbol", ondelete="CASCADE"), index=True)
    
    # Route Alpha: Structural Economics & Law (-100 to +100)
    alpha_score: Mapped[float] = mapped_column(Float, nullable=False)
    alpha_rationale: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Route Beta: Behavioral Psychology & Narrative (-100 to +100)
    beta_score: Mapped[float] = mapped_column(Float, nullable=False)
    beta_rationale: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Route Gamma: Philosophical Complexity & Tail Risk (-100 to +100)
    gamma_score: Mapped[float] = mapped_column(Float, nullable=False)
    gamma_rationale: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Consensus & Synthesis
    final_score: Mapped[float] = mapped_column(Float, nullable=False)
    disagreement_std: Mapped[float] = mapped_column(Float, default=0.0)
    gamma_vetoed: Mapped[bool] = mapped_column(Boolean, default=False)
    action_taken: Mapped[str] = mapped_column(String(20), nullable=False)  # BUY, SELL, HOLD, VETOED
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
