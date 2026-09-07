"""Backtest runner that operates directly on local CSV files.
100% Free, zero cloud cost, loads data via HistoricalCSVLoader.
"""

import sys
import os

sys.path.insert(0, ".")
from app.services.data_ingestion.csv_loader import csv_loader
from app.services.features.technical import TechnicalFeatureEngine
from app.services.backtesting.engine import EventDrivenBacktester
from app.services.cognitive_triad.orchestrator import CognitiveTriadOrchestrator


def run_csv_backtest(csv_path: str, symbol: str = "NABIL"):
    print("=" * 75)
    print(f"NEPSE COGNITIVE TRIAD: LOCAL CSV BACKTEST RUNNER ({symbol})")
    print("Zero-Cost Architecture: Local File Ingestion & Deterministic Execution")
    print("=" * 75)

    # 1. Load Local Historical CSV
    raw_bars = csv_loader.load_csv(csv_path, symbol=symbol)
    print(f"[*] Loaded {len(raw_bars)} historical bars from {os.path.basename(csv_path)}")

    # 2. Compute Technical Indicators locally
    enriched_bars = TechnicalFeatureEngine.compute_all(raw_bars)

    # 3. Cognitive Triad Strategy Function
    orchestrator = CognitiveTriadOrchestrator()
    memo_samples = []

    def strategy(bar, positions, available_cash):
        features = {
            "trend_bullish": bar.get("trend_bullish", 1),
            "volume_ratio": bar.get("volume_ratio", 1.5),
            "volatility_20": bar.get("volatility_20", 0.016),
            "volume_spike": bar.get("volume_spike", 0),
            "rsi_14": bar.get("rsi_14", 55.0),
            "candle_position": bar.get("candle_position", 0.80),
            "has_pending_action": 1 if bar["timestamp"].day < 12 else 0,
            "action_value_pct": 12.0,
            "days_to_book_close": 9,
            "urgency_score": 0.70,
            "ltp": bar["close"],
            "prev_close": bar["prev_close"],
            "current_sector_exposure": 0.08,
        }

        decision = orchestrator.decide(features, symbol=symbol)

        if len(memo_samples) < 2 and decision["action"] != "HOLD":
            memo_samples.append(decision)

        if decision["action"] == "BUY" and symbol not in positions:
            alloc = available_cash * 0.20
            qty = int(alloc / bar["close"])
            if qty >= 10:
                return {"action": "BUY", "symbol": symbol, "quantity": qty, "limit_price": bar["close"]}

        return None

    # 4. Run Backtester with NPR 13.3 Million Virtual Capital
    backtester = EventDrivenBacktester(initial_capital=13300000.0)
    results = backtester.run(strategy, enriched_bars)

    print(f"Starting Capital           : NPR {backtester.initial_capital:,.2f} ($100k USD)")
    print(f"Ending Portfolio Equity    : NPR {backtester.equity_curve[-1]:,.2f}")
    print(f"Cumulative Return          : {results.total_return_pct:+.2f}%")
    print(f"Max Drawdown               : {results.max_drawdown_pct:.2f}%")
    print(f"Total Completed Trades     : {results.total_trades}")
    print(f"Total Friction Fees Paid   : NPR {results.total_fees_paid:,.2f}")
    print("-" * 75)

    if memo_samples:
        print("\n[SAMPLE LOCAL AI STRATEGIC MEMO GENERATED]")
        print(memo_samples[0]["strategic_memo"])
    print("=" * 75)


if __name__ == "__main__":
    csv_file = os.path.join("data", "nabil_historical_100.csv")
    run_csv_backtest(csv_file, symbol="NABIL")
