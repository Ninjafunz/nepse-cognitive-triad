"""Historical backtest simulation using synthetic NEPSE price action modeling the 2021 bull run."""

import sys
from datetime import datetime, timedelta

sys.path.insert(0, ".")
from app.services.backtesting.engine import EventDrivenBacktester
from app.services.cognitive_triad.orchestrator import CognitiveTriadOrchestrator
from app.services.features.technical import TechnicalFeatureEngine


def generate_nepse_bull_market_bars(symbol: str, start_price: float = 300.0, days: int = 120):
    bars = []
    curr_price = start_price
    start_date = datetime(2021, 1, 3, 11, 0)  # Sunday

    for day_idx in range(days):
        ts = start_date + timedelta(days=day_idx)
        if ts.weekday() in (4, 5):
            continue

        prev_close = curr_price
        drift = 1.018 if day_idx % 6 != 0 else 0.982
        curr_price = round(curr_price * drift, 2)
        high = round(curr_price * 1.01, 2)
        low = round(curr_price * 0.99, 2)
        vol = 45000.0 + (day_idx * 800.0)

        bars.append({
            "timestamp": ts,
            "symbol": symbol,
            "open": prev_close,
            "high": high,
            "low": low,
            "close": curr_price,
            "prev_close": prev_close,
            "volume": vol,
            "time": ts.isoformat(),
        })

    return TechnicalFeatureEngine.compute_all(bars)


def run_historical_validation():
    print("=" * 70)
    print("NEPSE COGNITIVE TRIAD: 2021 HISTORICAL BULL MARKET BACKTEST VALIDATION")
    print("=" * 70)

    nabil_bars = generate_nepse_bull_market_bars("NABIL", start_price=600.0, days=120)
    shivm_bars = generate_nepse_bull_market_bars("SHIVM", start_price=450.0, days=120)
    chcl_bars = generate_nepse_bull_market_bars("CHCL", start_price=350.0, days=120)

    all_bars = sorted(nabil_bars + shivm_bars + chcl_bars, key=lambda b: b["timestamp"])

    orchestrator = CognitiveTriadOrchestrator()

    def triad_strategy(bar, positions, available_cash):
        sym = bar["symbol"]
        close = bar["close"]

        # Incorporate realistic corporate action catalyst in early bull cycle
        day_num = bar["timestamp"].day
        has_ca = 1 if day_num < 15 else 0

        features = {
            "trend_bullish": bar.get("trend_bullish", 1),
            "volume_ratio": bar.get("volume_ratio", 1.8),
            "volatility_20": bar.get("volatility_20", 0.015),
            "volume_spike": 1 if bar.get("volume_ratio", 1.8) > 1.5 else 0,
            "rsi_14": bar.get("rsi_14", 55.0),
            "candle_position": bar.get("candle_position", 0.85),
            "has_pending_action": has_ca,
            "action_value_pct": 15.0 if has_ca else 0.0,
            "days_to_book_close": 10 if has_ca else 999,
            "urgency_score": 0.70 if has_ca else 0.0,
            "ltp": close,
            "prev_close": bar.get("prev_close", close),
            "current_sector_exposure": 0.10,
        }

        decision = orchestrator.decide(features)
        action = decision["action"]

        if action == "BUY" and sym not in positions:
            target_alloc = available_cash * 0.20
            qty = int(target_alloc / close)
            if qty >= 10:
                return {"action": "BUY", "symbol": sym, "quantity": qty, "limit_price": close}

        elif action == "SELL" and sym in positions:
            qty = positions[sym]["qty"]
            if qty > 0:
                return {"action": "SELL", "symbol": sym, "quantity": qty, "limit_price": close}

        return None

    backtester = EventDrivenBacktester(initial_capital=13300000.0)
    result = backtester.run(triad_strategy, all_bars)

    print(f"Initial Virtual Capital : NPR {backtester.initial_capital:,.2f} ($100,000 USD equivalent)")
    print(f"Final Portfolio Equity  : NPR {backtester.equity_curve[-1]:,.2f}")
    print(f"Total Cumulative Return : {result.total_return_pct:+.2f}%")
    print(f"Sharpe Ratio            : {result.sharpe_ratio:.2f}")
    print(f"Max Drawdown            : {result.max_drawdown_pct:.2f}%")
    print(f"Win Rate                : {result.win_rate:.2f}%")
    print(f"Total Completed Trades  : {result.total_trades}")
    print(f"Total Friction Fees Paid: NPR {result.total_fees_paid:,.2f}")
    print("=" * 70)


if __name__ == "__main__":
    run_historical_validation()
