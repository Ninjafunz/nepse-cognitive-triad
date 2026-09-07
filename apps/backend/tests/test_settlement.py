"""Unit tests for NEPSE T+2 settlement calendar logic."""

import pytest
from datetime import date
from app.services.settlement.t2_engine import T2SettlementEngine


def test_t2_settlement_standard_weekday():
    engine = T2SettlementEngine()
    # Sunday (2026-09-06) -> T+1 is Monday (2026-09-07), T+2 is Tuesday (2026-09-08)
    trade_date = date(2026, 9, 6)  # Sunday
    settlement = engine.calculate_settlement_date(trade_date)
    assert settlement == date(2026, 9, 8)  # Tuesday


def test_t2_settlement_skips_friday_saturday_nepal_weekend():
    engine = T2SettlementEngine()
    # Wednesday (2026-09-09) -> T+1 is Thursday (2026-09-10).
    # Friday & Saturday are closed.
    # T+2 is Sunday (2026-09-13).
    trade_date = date(2026, 9, 9)  # Wednesday
    settlement = engine.calculate_settlement_date(trade_date)
    assert settlement == date(2026, 9, 13)  # Sunday


def test_t2_settlement_skips_nepali_public_holiday():
    dashain_holiday = date(2026, 10, 20)  # Tuesday holiday
    engine = T2SettlementEngine(public_holidays={dashain_holiday})

    # Sunday trade date
    trade_date = date(2026, 10, 18)  # Sunday
    # T+1: Monday (2026-10-19)
    # Tuesday (2026-10-20) skipped due to holiday
    # T+2: Wednesday (2026-10-21)
    settlement = engine.calculate_settlement_date(trade_date)
    assert settlement == date(2026, 10, 21)
