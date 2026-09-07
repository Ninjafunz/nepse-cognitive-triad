"""Comprehensive Unit Tests for Features, Backtester, and Cognitive Triad Agents."""

import unittest
from datetime import datetime, date, timedelta
from app.services.features.technical import TechnicalFeatureEngine
from app.services.features.corporate_actions import CorporateActionFeatureEngine
from app.services.backtesting.engine import EventDrivenBacktester
from app.services.cognitive_triad.alpha import RouteAlpha
from app.services.cognitive_triad.beta import RouteBeta
from app.services.cognitive_triad.gamma import RouteGamma
from app.services.cognitive_triad.orchestrator import CognitiveTriadOrchestrator


class TestPhase2FeaturesAndBacktesting(unittest.TestCase):

    def test_01_technical_indicators_rsi_ema(self):
        sample_bars = []
        base_price = 500.0
        for i in range(30):
            p = base_price + (i * 2.0)
            sample_bars.append({
                "time": f"2026-09-01T11:{i:02d}:00Z",
                "open": p - 1.0,
                "high": p + 2.0,
                "low": p - 1.0,
                "close": p,
                "volume": 1000.0 + (i * 50),
            })
        enriched = TechnicalFeatureEngine.compute_all(sample_bars)
        last_bar = enriched[-1]

        self.assertIn("rsi_14", last_bar)
        self.assertIn("ema_20", last_bar)
        self.assertIn("ema_50", last_bar)
        self.assertIn("trend_bullish", last_bar)
        self.assertEqual(last_bar["trend_bullish"], 1)  # Uptrend

    def test_02_corporate_action_urgency_score(self):
        engine = CorporateActionFeatureEngine()
        today = date(2026, 9, 8)
        close_date = today + timedelta(days=10)

        feats = engine.compute_from_record("BONUS_SHARE", 15.0, close_date, today)
        self.assertEqual(feats["has_pending_action"], 1)
        self.assertEqual(feats["days_to_book_close"], 10)
        self.assertEqual(feats["action_value_pct"], 15.0)
        # Urgency: max(0, 30 - 10) / 30 = 20 / 30 ~ 0.67
        self.assertAlmostEqual(feats["urgency_score"], 0.67, places=2)

    def test_03_backtester_circuit_breaker_rejection(self):
        bt = EventDrivenBacktester(initial_capital=1000000.0)
        ts = datetime(2026, 9, 8, 11, 30)

        # Prev close: 500. Limit price: 600 (+20% > 10% circuit limit)
        trade = bt.execute_buy(
            timestamp=ts,
            symbol="NABIL",
            quantity=100,
            limit_price=600.0,
            prev_close=500.0,
        )
        self.assertIsNone(trade)
        self.assertEqual(len(bt.trades), 0)

    def test_04_backtester_settled_cash_limit_rejection(self):
        bt = EventDrivenBacktester(initial_capital=50000.0)
        ts = datetime(2026, 9, 8, 11, 30)

        # Attempt to buy 1000 shares @ 500 NPR = 500,000 NPR > 50,000 NPR
        trade = bt.execute_buy(
            timestamp=ts,
            symbol="NABIL",
            quantity=1000,
            limit_price=500.0,
            prev_close=500.0,
        )
        self.assertIsNone(trade)
        self.assertEqual(len(bt.trades), 0)

    def test_05_backtester_successful_buy_and_position(self):
        bt = EventDrivenBacktester(initial_capital=1000000.0)
        ts = datetime(2026, 9, 8, 11, 30)

        trade = bt.execute_buy(
            timestamp=ts,
            symbol="NABIL",
            quantity=100,
            limit_price=500.0,
            prev_close=500.0,
        )
        self.assertIsNotNone(trade)
        self.assertEqual(trade.side, "BUY")
        self.assertIn("NABIL", bt.positions)
        self.assertEqual(bt.positions["NABIL"]["qty"], 100)

    def test_06_backtester_no_shorting_enforcement(self):
        bt = EventDrivenBacktester(initial_capital=1000000.0)
        ts = datetime(2026, 9, 8, 11, 30)

        # Try to sell 50 shares of SHIVM without owning it
        trade = bt.execute_sell(
            timestamp=ts,
            symbol="SHIVM",
            quantity=50,
            limit_price=450.0,
            prev_close=450.0,
        )
        self.assertIsNone(trade)

    def test_07_backtester_sell_creates_t2_settlement(self):
        bt = EventDrivenBacktester(initial_capital=1000000.0)
        ts_buy = datetime(2026, 9, 6, 11, 30)  # Sunday
        ts_sell = datetime(2026, 9, 7, 11, 30)  # Monday

        bt.execute_buy(ts_buy, "NABIL", 100, 500.0, 500.0)
        sell_trade = bt.execute_sell(ts_sell, "NABIL", 100, 520.0, 500.0)

        self.assertIsNotNone(sell_trade)
        self.assertEqual(len(bt.pending_settlements), 1)
        # Sells on Monday (9/7) settle on Wednesday (9/9)
        self.assertEqual(bt.pending_settlements[0]["settle_date"], date(2026, 9, 9))

    def test_08_route_alpha_scoring(self):
        alpha = RouteAlpha()
        features = {
            "trend_bullish": 1,
            "volume_ratio": 2.0,
            "volatility_20": 0.015,
            "has_pending_action": 1,
            "action_value_pct": 12.0,
            "days_to_book_close": 7,
            "ltp": 510.0,
            "prev_close": 500.0,
        }
        res = alpha.evaluate(features)
        self.assertEqual(res["agent"], "ALPHA")
        self.assertGreater(res["score"], 50.0)
        self.assertIn("Keynes (1936)", res["literature_cited"])

    def test_09_route_beta_sentiment_and_shiller_urgency(self):
        beta = RouteBeta()
        features = {
            "volume_spike": 1,
            "rsi_14": 40.0,
            "urgency_score": 0.8,
            "candle_position": 0.9,
        }
        res = beta.evaluate(features)
        self.assertEqual(res["agent"], "BETA")
        self.assertGreater(res["score"], 50.0)
        self.assertIn("Shiller (2019)", res["literature_cited"])

    def test_10_route_gamma_taleb_veto_on_fragility(self):
        gamma = RouteGamma()
        # High volatility regime > 6%
        features = {"volatility_20": 0.075}
        res = gamma.evaluate(features)
        self.assertEqual(res["agent"], "GAMMA")
        self.assertTrue(res["veto"])
        self.assertLessEqual(res["score"], -50.0)

    def test_11_orchestrator_consensus_and_veto(self):
        orchestrator = CognitiveTriadOrchestrator()

        # Case A: Taleb Veto engaged
        veto_features = {
            "volatility_20": 0.08,
            "trend_bullish": 1,
            "volume_ratio": 2.5,
        }
        decision_veto = orchestrator.decide(veto_features)
        self.assertEqual(decision_veto["action"], "HOLD")
        self.assertEqual(decision_veto["reason"], "GAMMA_VETO")
        self.assertTrue(decision_veto["gamma_vetoed"])

        # Case B: Harmonious Bullish Consensus
        bullish_features = {
            "trend_bullish": 1,
            "volume_ratio": 1.8,
            "volatility_20": 0.015,
            "volume_spike": 1,
            "rsi_14": 52.0,
            "candle_position": 0.85,
            "has_pending_action": 1,
            "action_value_pct": 15.0,
            "days_to_book_close": 8,
            "urgency_score": 0.7,
            "ltp": 505.0,
            "prev_close": 500.0,
        }
        decision_buy = orchestrator.decide(bullish_features)
        self.assertEqual(decision_buy["action"], "BUY")
        self.assertEqual(decision_buy["reason"], "CONSENSUS")
        self.assertGreaterEqual(decision_buy["final_score"], 40.0)


if __name__ == "__main__":
    unittest.main()
