"""Route Gamma: The Philosophical Systemist.
Disciplines: Epistemology, Complexity Science, Risk Philosophy.
Literature: Taleb, Soros, Popper, W. Brian Arthur.
HOLDS VETO POWER.
"""

from typing import Dict, Any


class RouteGamma:
    """THE PHILOSOPHICAL SYSTEMIST
    Evaluates: tail risk, fragility, reflexivity, epistemic uncertainty.
    HOLDS UNILATERAL VETO POWER.
    """

    WEIGHT = 0.25
    VETO_THRESHOLD = -50.0

    def evaluate(self, features: Dict[str, Any]) -> Dict[str, Any]:
        score = 0.0
        rationale = []
        veto = False

        volatility = float(features.get("volatility_20", 0.0))

        # 1. Volatility Fragility vs Antifragility (Taleb)
        if volatility > 0.06:
            score -= 60.0
            veto = True
            rationale.append(f"Volatility at {volatility:.2%}. Taleb: This is a fragile regime. Asymmetric downside risk. VETO ENGAGED.")
        elif volatility > 0.04:
            score -= 30.0
            rationale.append("Elevated volatility. Taleb recommends reducing position size to maintain antifragility.")
        elif 0.0 < volatility <= 0.025:
            # Low volatility baseline conviction
            score += 20.0
            rationale.append("Low volatility regime. System exhibits structural stability.")

        # 2. Concentration Risk (Complex Adaptive Systems)
        sector_exposure = float(features.get("current_sector_exposure", 0.0))
        if sector_exposure > 0.30:
            score -= 40.0
            rationale.append(f"Portfolio already {sector_exposure:.0%} exposed to this sector. Complex systems theory: correlated failures risk.")

        # 3. Soros' Reflexivity Check
        if float(features.get("volume_ratio", 0.0)) > 2.0 and float(features.get("rsi_14", 50.0)) > 80.0:
            score -= 35.0
            rationale.append("Extreme volume + extreme RSI. Soros' Reflexivity: positive feedback loop may be near exhaustion. Heightened reversal risk.")

        # 4. Popper's Falsification
        if features.get("has_pending_action") == 1 and (features.get("days_to_book_close") or 999) <= 3:
            score -= 20.0
            rationale.append("Only 3 days to book close. Popper: thesis is approaching its falsification window. Post-event uncertainty is extreme.")

        if score <= self.VETO_THRESHOLD:
            veto = True

        return {
            "agent": "GAMMA",
            "score": max(-100.0, min(100.0, score)),
            "rationale": rationale,
            "veto": veto,
            "literature_cited": ["Taleb (2012)", "Soros (1987)", "Popper (1934)"],
        }
