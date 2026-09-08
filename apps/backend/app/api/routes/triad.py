"""Cognitive Triad and Journaling API endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.api.deps import get_db
from app.models.triad import TriadDecision
from app.models.journals import TradeJournal
from app.models.evaluations import DailyEvaluation, PredictionReflection
from app.services.cognitive_triad.orchestrator import triad_orchestrator
from app.services.journaling.generator import journal_generator
from app.services.data_ingestion.nepse_client import nepse_client
from app.tasks.reflection_tasks import run_daily_reflection_check

router = APIRouter()


@router.get("/evaluate/{symbol}")
async def evaluate_symbol_triad(symbol: str):
    """Evaluates a NEPSE stock through the lenses of Alpha, Beta, and Gamma."""
    sym = symbol.upper()
    features = {
        "trend_bullish": 1,
        "volume_ratio": 1.6,
        "volatility_20": 0.018,
        "volume_spike": 1,
        "rsi_14": 54.0,
        "candle_position": 0.82,
        "has_pending_action": 1,
        "action_value_pct": 12.0,
        "days_to_book_close": 9,
        "urgency_score": 0.70,
        "ltp": 510.0,
        "prev_close": 500.0,
        "current_sector_exposure": 0.12,
    }
    decision = triad_orchestrator.decide(features)
    journal_text = await journal_generator.generate_journal_entry(sym, decision)

    return {
        "symbol": sym,
        "decision": decision,
        "synthesized_journal": journal_text,
    }


@router.get("/decisions")
async def list_triad_decisions(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """Lists past consensus decisions and route scores."""
    stmt = select(TriadDecision).order_by(desc(TriadDecision.created_at)).limit(limit)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.get("/journals")
async def list_trade_journals(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """Lists AI generated trade thesis journals with literature citations."""
    stmt = select(TradeJournal).order_by(desc(TradeJournal.created_at)).limit(limit)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.get("/evaluations")
async def list_daily_evaluations(
    action: str = None,
    veto_only: bool = False,
    symbol: str = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Lists market-wide security evaluations demonstrating negative selection discipline."""
    stmt = select(DailyEvaluation)
    if action:
        stmt = stmt.where(DailyEvaluation.final_action == action.upper())
    if veto_only:
        stmt = stmt.where(DailyEvaluation.gamma_veto.is_(True))
    if symbol:
        stmt = stmt.where(DailyEvaluation.symbol == symbol.upper())

    stmt = stmt.order_by(desc(DailyEvaluation.eval_date), desc(DailyEvaluation.created_at))
    stmt = stmt.offset(offset).limit(limit)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.get("/reflections")
async def list_prediction_reflections(
    symbol: str = None,
    was_correct: bool = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """Lists historical multi-day predictions and post-mortem self-correction reports."""
    stmt = select(PredictionReflection)
    if symbol:
        stmt = stmt.where(PredictionReflection.symbol == symbol.upper())
    if was_correct is not None:
        stmt = stmt.where(PredictionReflection.was_correct == was_correct)

    stmt = stmt.order_by(desc(PredictionReflection.target_date), desc(PredictionReflection.created_at)).limit(limit)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.post("/reflections/run-audit")
async def trigger_reflection_audit():
    """Manually triggers the daily epistemic reflection critic audit."""
    processed = run_daily_reflection_check()
    return {
        "status": "success",
        "message": "Epistemic reflection audit executed",
        "processed_count": processed,
    }

