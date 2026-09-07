"""Standalone unit tests for pure domain logic without third-party dependencies."""

import unittest
from datetime import date, timedelta


class T2SettlementEngine:
    def __init__(self, public_holidays=None):
        self.public_holidays = public_holidays or set()

    def is_business_day(self, d: date) -> bool:
        # Friday (4) and Saturday (5) are market off days in Nepal
        if d.weekday() in (4, 5):
            return False
        if d in self.public_holidays:
            return False
        return True

    def calculate_settlement_date(self, trade_date: date) -> date:
        curr = trade_date
        settlement_days_added = 0
        while settlement_days_added < 2:
            curr += timedelta(days=1)
            if self.is_business_day(curr):
                settlement_days_added += 1
        return curr


class SlippageAndFeeCalculator:
    BROKER_COMMISSION_PCT = 0.0037
    SEBON_FEE_PCT = 0.00015
    DP_CHARGE_NPR = 25.0

    def calculate_fees(self, trade_value: float, side: str):
        broker_fee = trade_value * self.BROKER_COMMISSION_PCT
        sebon_fee = trade_value * self.SEBON_FEE_PCT
        dp_charge = self.DP_CHARGE_NPR if side.upper() == "SELL" else 0.0

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


class TestNepseDomainLogic(unittest.TestCase):
    def test_t2_settlement_standard_days(self):
        engine = T2SettlementEngine()
        trade_date = date(2026, 9, 6)  # Sunday
        settlement = engine.calculate_settlement_date(trade_date)
        self.assertEqual(settlement, date(2026, 9, 8))  # Tuesday

    def test_t2_settlement_crosses_nepal_weekend(self):
        engine = T2SettlementEngine()
        trade_date = date(2026, 9, 9)  # Wednesday
        settlement = engine.calculate_settlement_date(trade_date)
        # Friday/Saturday closed -> Sunday
        self.assertEqual(settlement, date(2026, 9, 13))

    def test_fee_calculations(self):
        calc = SlippageAndFeeCalculator()
        trade_val = 100000.0

        buy_fees = calc.calculate_fees(trade_val, "BUY")
        self.assertEqual(buy_fees["broker_commission"], 370.0)
        self.assertEqual(buy_fees["sebon_fee"], 15.0)
        self.assertEqual(buy_fees["dp_charge"], 0.0)
        self.assertEqual(buy_fees["total_fees"], 385.0)

        sell_fees = calc.calculate_fees(trade_val, "SELL")
        self.assertEqual(sell_fees["dp_charge"], 25.0)
        self.assertEqual(sell_fees["total_fees"], 410.0)

    def test_buying_power_math(self):
        today = date(2026, 9, 8)
        future = date(2026, 9, 10)
        entries = [
            {"amount": 13300000.0, "settled": today},
            {"amount": 500000.0, "settled": future},
            {"amount": -200000.0, "settled": today},
        ]
        settled_cash = sum(e["amount"] for e in entries if e["settled"] <= today)
        buying_power = max(0.0, settled_cash)
        self.assertEqual(buying_power, 13100000.0)


if __name__ == "__main__":
    unittest.main()
