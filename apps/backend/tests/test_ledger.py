"""Unit tests for ledger math, initial deposit, and buying power availability."""

import pytest
from datetime import date, timedelta


def test_buying_power_excludes_unsettled_funds():
    today = date.today()
    future_settlement = today + timedelta(days=2)

    # Simulated ledger entries
    ledger = [
        {"amount": 13300000.0, "settled_date": today},  # Settled deposit
        {"amount": 500000.0, "settled_date": future_settlement},  # Unsettled proceeds from sell
        {"amount": -200000.0, "settled_date": today},  # Settled debit
    ]

    settled_cash = sum(e["amount"] for e in ledger if e["settled_date"] <= today)
    unsettled_cash = sum(e["amount"] for e in ledger if e["settled_date"] > today)

    # Buying power is bounded strictly by settled funds
    available_buying_power = max(0.0, settled_cash)

    assert settled_cash == 13100000.0
    assert unsettled_cash == 500000.0
    assert available_buying_power == 13100000.0
