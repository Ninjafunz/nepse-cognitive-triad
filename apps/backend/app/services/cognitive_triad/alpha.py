"""Route Alpha: The Structural Rationalist.
Disciplines: Macroeconomics, Corporate Finance, Institutional Law.
Literature: Minsky, Keynes, Fama-French, Douglass North.
"""

from typing import Dict, Any


class RouteAlpha:
    """THE STRUCTURAL RATIONALIST
    Evaluates: liquidity conditions, regulatory shifts, fundamental value, trend momentum.
    """

    WEIGHT = 0.40  # Highest weight in consensus

    def evaluate(self, features: Dict[str, Any]) -> Dict[str, Any]:
        score = 0.0
        rationale = []

        # 1. Trend Momentum (Fama-French momentum factor)
        if features.get("trend_bullish") == 1:
            score += 25
            rationale.append("EMA crossover confirms structural uptrend. Aligns with Fama-French momentum premium.")

        # 2. Liquidity / Volume Confirmation (Keynes' Liquidity Preference)
        if features.get("volume_ratio", 0.0) > 1.5:
            score += 20
            rationale.append("Volume surge indicates liquidity preference shifting to this asset. Keynesian liquidity signal.")

        # 3. Volatility Regime (Minsky's Financial Instability)
        volatility = features.get("volatility_20", 0.0)
        if volatility > 0.05:
            score -= 30
            rationale.append(f"Volatility at {volatility:.2%}. Minsky framework suggests late-stage instability. Reducing exposure.")
        elif volatility < 0.02:
            score += 15
            rationale.append("Low volatility indicates stable credit conditions. Minsky's 'hedge finance' phase.")

        # 4. Corporate Action Catalyst
        if features.get("has_pending_action") == 1:
            value = features.get("action_value_pct", 0.0)
            days = features.get("days_to_book_close", 999)
            if days <= 14 and value >= 10:
                score += 30
                rationale.append(f"Corporate action catalyst: {value}% value, {days} days to book close. Structural undervaluation closing.")

        # 5. Circuit Breaker Proximity (Regulatory constraint)
        ltp = features.get("ltp", 0.0)
        prev_close = features.get("prev_close", ltp)
        if prev_close > 0:
            pct_change = (ltp - prev_close) / prev_close
            if pct_change > 0.08:
                score -= 50
                rationale.append("Approaching +10% circuit breaker. Regulatory constraint limits upside. Reducing Alpha score.")

        return {
            "agent": "ALPHA",
            "score": max(-100.0, min(100.0, score)),
            "rationale": rationale,
            "literature_cited": ["Minsky (1992)", "Fama & French (1993)", "Keynes (1936)"],
        }
