"""Realistic slippage and fee engine adhering to NEPSE rules."""

from typing import Dict, Any

try:
    from app.config import settings
    BROKER_COMMISSION = settings.BROKER_COMMISSION_PCT
    SEBON_FEE = settings.SEBON_FEE_PCT
    DP_CHARGE = settings.DP_CHARGE_NPR
except Exception:
    BROKER_COMMISSION = 0.0037
    SEBON_FEE = 0.00015
    DP_CHARGE = 25.0


class SlippageAndFeeCalculator:
    """Calculates broker commissions, SEBON regulatory fees, DP charges, and liquidity-based slippage."""

    def calculate_fees(self, trade_value: float, side: str) -> Dict[str, float]:
        broker_fee = trade_value * BROKER_COMMISSION
        sebon_fee = trade_value * SEBON_FEE
        dp_charge = DP_CHARGE if side.upper() == "SELL" else 0.0

        return {
            "broker_commission": round(broker_fee, 2),
            "sebon_fee": round(sebon_fee, 2),
            "dp_charge": float(dp_charge),
            "total_fees": round(broker_fee + sebon_fee + dp_charge, 2),
        }

    def estimate_slippage_pct(self, order_qty: int, avg_daily_volume: float) -> float:
        if avg_daily_volume <= 0:
            return 0.005

        volume_ratio = order_qty / avg_daily_volume
        if volume_ratio < 0.01:
            return 0.0015
        elif volume_ratio < 0.05:
            return 0.005
        else:
            return min(0.025, 0.005 + (volume_ratio * 0.05))

    def simulate_execution_price(self, ltp: float, side: str, slippage_pct: float) -> float:
        if side.upper() == "BUY":
            fill_price = ltp * (1.0 + slippage_pct)
        else:
            fill_price = ltp * (1.0 - slippage_pct)

        return round(fill_price, 2)


fee_calculator = SlippageAndFeeCalculator()
