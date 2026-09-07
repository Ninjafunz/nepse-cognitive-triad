"""Route Beta: The Behavioral Synthesizer.
Disciplines: Behavioral Psychology, Narrative Economics, Social History.
Literature: Kahneman, Shiller, Le Bon, Mackay, Dalio.
"""

from typing import Dict, Any


class RouteBeta:
    """THE BEHAVIORAL SYNTHESIZER
    Evaluates: retail sentiment, herd behavior, narrative urgency, overconfidence bias.
    """

    WEIGHT = 0.35

    def evaluate(self, features: Dict[str, Any]) -> Dict[str, Any]:
        score = 0.0
        rationale = []

        # 1. Volume Spike = Herd Mentality (Le Bon's Crowd Psychology)
        if features.get("volume_spike") == 1:
            score += 30
            rationale.append("Volume spike detected. Le Bon's crowd psychology: collective behavior overriding individual rationality.")

        # 2. RSI Extremes = Cognitive Bias (Kahneman's Prospect Theory)
        rsi = float(features.get("rsi_14", 50.0))
        if rsi > 75:
            score -= 25
            rationale.append(f"RSI at {rsi:.0f}. Retail investors exhibiting overconfidence bias. Kahneman: probability weighting distorted at extremes.")
        elif rsi < 25:
            score += 25
            rationale.append(f"RSI at {rsi:.0f}. Loss aversion creating panic selling. Kahneman: potential mean-reversion opportunity.")

        # 3. Corporate Action Urgency = Narrative Economics (Shiller)
        urgency = float(features.get("urgency_score", 0.0))
        if urgency > 0.5:
            score += 25
            rationale.append(f"Corporate action urgency score: {urgency:.2f}. Shiller's Narrative Economics: story-driven buying accelerating as book close approaches.")

        # 4. Candle Position = Immediate Sentiment
        candle_pos = float(features.get("candle_position", 0.5))
        if candle_pos > 0.8:
            score += 15
            rationale.append("Price closing near candle high. Immediate bullish sentiment from retail participants.")
        elif candle_pos < 0.2:
            score -= 15
            rationale.append("Price closing near candle low. Bearish sentiment dominating.")

        return {
            "agent": "BETA",
            "score": max(-100.0, min(100.0, score)),
            "rationale": rationale,
            "literature_cited": ["Kahneman & Tversky (1979)", "Shiller (2019)", "Le Bon (1895)"],
        }
