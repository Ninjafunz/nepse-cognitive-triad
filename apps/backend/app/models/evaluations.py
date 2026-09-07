"""SQLAlchemy ORM models for the Daily Decision Matrix and Epistemic Reflection Engine.
Captures non-action discipline and post-mortem self-correction loops.
"""

import uuid
from datetime import datetime, date
from sqlalchemy import (
    Column,
    String,
    Numeric,
    Boolean,
    Text,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class DailyEvaluation(Base):
    """Logs EVERY security evaluated by the Cognitive Triad each market session.
    Proves strategic non-action discipline (evaluating 50 stocks, standing aside on 48).
    """

    __tablename__ = "daily_evaluations"

    evaluation_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    eval_date = Column(Date, nullable=False, default=date.today)
    symbol = Column(String(10), nullable=False)
    sector = Column(String(50), nullable=True)

    # Triad Disciplinary Scores
    alpha_score = Column(Numeric(5, 2), nullable=False)
    beta_score = Column(Numeric(5, 2), nullable=False)
    gamma_score = Column(Numeric(5, 2), nullable=False)
    gamma_veto = Column(Boolean, default=False, nullable=False)

    # Final Decision: BUY, SELL, HOLD, NO_ACTION
    final_action = Column(String(20), nullable=False)

    # Qualitative Strategic Reason
    primary_reason = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("eval_date", "symbol", name="uq_daily_eval_date_symbol"),
    )


class PredictionReflection(Base):
    """The Epistemic Reflection Engine: tracks multi-day price predictions and
    forces the AI to generate literature-grounded post-mortems on failed theses.
    """

    __tablename__ = "prediction_reflections"

    reflection_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    evaluation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("daily_evaluations.evaluation_id", ondelete="CASCADE"),
        nullable=True,
    )

    symbol = Column(String(10), nullable=False)
    prediction_date = Column(Date, nullable=False)
    target_date = Column(Date, nullable=False)  # T+5 trading days later

    # What the AI thought would happen
    predicted_thesis = Column(Text, nullable=False)
    expected_direction = Column(String(10), nullable=False)  # UP / DOWN

    # What actually occurred in the market
    actual_return_pct = Column(Numeric(5, 2), nullable=True)
    was_correct = Column(Boolean, nullable=True)

    # The AI's Post-Mortem Self-Correction Report
    reflection_journal = Column(Text, nullable=True)
    failed_route = Column(String(20), nullable=True)  # ALPHA, BETA, or GAMMA
    epistemic_concept = Column(String(100), nullable=True)  # e.g., Soros Reflexivity
    corrective_action = Column(Text, nullable=True)

    reflected_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
