"""Corporate Action Feature Engine.
Feeds Route Alpha (fundamental catalysts) and Route Beta (narrative urgency).
"""

from datetime import date
from typing import Dict, Any, Optional

try:
    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.models.corporate_actions import CorporateAction
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False


class CorporateActionFeatureEngine:
    """Computes corporate action signals (dividends, bonus shares, right shares)."""

    ACTION_TYPE_MAP = {
        "CASH_DIVIDEND": 1,
        "dividend": 1,
        "BONUS_SHARE": 2,
        "bonus": 2,
        "RIGHT_SHARE": 3,
        "right": 3,
        "STOCK_SPLIT": 4,
        "split": 4,
    }

    async def get_action_features_async(
        self, session: Any, symbol: str, current_date: date
    ) -> Dict[str, Any]:
        """Queries database for upcoming corporate action on symbol."""
        if not HAS_SQLALCHEMY:
            return self._empty_action_features()

        stmt = (
            select(CorporateAction)
            .where(
                CorporateAction.symbol == symbol,
                CorporateAction.book_close_date >= current_date,
            )
            .order_by(CorporateAction.book_close_date)
            .limit(1)
        )
        res = await session.execute(stmt)
        action = res.scalar_one_or_none()

        if not action:
            return self._empty_action_features()

        return self.compute_from_record(
            action_type=action.action_type,
            value=action.value,
            book_close_date=action.book_close_date,
            current_date=current_date,
        )

    def compute_from_record(
        self, action_type: str, value: float, book_close_date: Optional[date], current_date: date
    ) -> Dict[str, Any]:
        if not book_close_date:
            return self._empty_action_features()

        days_to_close = (book_close_date - current_date).days
        urgency_score = max(0.0, float(30 - max(0, days_to_close))) / 30.0

        return {
            "has_pending_action": 1,
            "days_to_book_close": max(0, days_to_close),
            "action_value_pct": float(value or 0.0),
            "action_type_encoded": self.ACTION_TYPE_MAP.get(action_type, 0),
            "urgency_score": round(urgency_score, 2),
        }

    def _empty_action_features(self) -> Dict[str, Any]:
        return {
            "has_pending_action": 0,
            "days_to_book_close": None,
            "action_value_pct": 0.0,
            "action_type_encoded": 0,
            "urgency_score": 0.0,
        }


corporate_feature_engine = CorporateActionFeatureEngine()
