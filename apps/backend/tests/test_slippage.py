"""Unit tests for slippage, broker commissions, and execution pricing."""

import pytest
from app.services.trading.slippage import SlippageAndFeeCalculator


def test_calculate_fees_buy():
    calc = SlippageAndFeeCalculator()
    trade_val = 100000.0  # NPR 100,000
    fees = calc.calculate_fees(trade_val, side="BUY")

    # 0.37% broker = 370.0
    assert fees["broker_commission"] == 370.0
    # 0.015% SEBON = 15.0
    assert fees["sebon_fee"] == 15.0
    # DP charge is 0 on BUY in NEPSE
    assert fees["dp_charge"] == 0.0
    assert fees["total_fees"] == 385.0


def test_calculate_fees_sell_includes_dp_charge():
    calc = SlippageAndFeeCalculator()
    trade_val = 100000.0  # NPR 100,000
    fees = calc.calculate_fees(trade_val, side="SELL")

    assert fees["broker_commission"] == 370.0
    assert fees["sebon_fee"] == 15.0
    # DP charge Rs 25 on SELL
    assert fees["dp_charge"] == 25.0
    assert fees["total_fees"] == 410.0


def test_slippage_and_price_direction():
    calc = SlippageAndFeeCalculator()
    ltp = 500.0

    # Low volume trade: 0.15% slippage
    slippage = calc.estimate_slippage_pct(order_qty=50, avg_daily_volume=50000)
    assert slippage < 0.005

    buy_price = calc.simulate_execution_price(ltp, "BUY", slippage)
    sell_price = calc.simulate_execution_price(ltp, "SELL", slippage)

    # Buys pay more, sells receive less
    assert buy_price > ltp
    assert sell_price < ltp
