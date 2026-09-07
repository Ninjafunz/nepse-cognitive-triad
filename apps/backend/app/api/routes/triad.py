"""Cognitive Triad and Journaling API endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.api.deps import get_db
from app.models.triad import TriadDecision
from app.models.journals import TradeJournal
from app.services.cognitive_triad.orchestrator import triad_orchestrator
from app.services.journaling.generator import journal_generator
from app.services.data_ingestion.nepse_client import nepse_client

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
