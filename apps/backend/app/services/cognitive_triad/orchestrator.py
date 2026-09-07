"""Cognitive Triad Consensus Orchestrator with Local Llama-3 (Ollama) Journaling.
Combines Route Alpha, Beta, Gamma (Taleb Veto), and Local LLM synthesis.
"""

import statistics
from typing import Dict, Any
from app.services.cognitive_triad.alpha import RouteAlpha
from app.services.cognitive_triad.beta import RouteBeta
from app.services.cognitive_triad.gamma import RouteGamma
from app.services.journaling.local_llm import local_journal_generator


class CognitiveTriadOrchestrator:
    """THE COGNITIVE PROSTHETIC INTERFACE
    Gamma holds veto. Alpha has highest weight. Beta bridges sentiment.
    Connects to local Llama-3 (Ollama) to draft strategic memos.
    """

    TRADE_THRESHOLD = 40.0   # Minimum consensus score to trigger a trade
    MAX_DISAGREEMENT = 45.0  # Max std deviation between routes (high = no conviction)

    def __init__(self):
        self.alpha = RouteAlpha()
        self.beta = RouteBeta()
        self.gamma = RouteGamma()

    def decide(self, features: Dict[str, Any], symbol: str = "NABIL") -> Dict[str, Any]:
        alpha_res = self.alpha.evaluate(features)
        beta_res = self.beta.evaluate(features)
        gamma_res = self.gamma.evaluate(features)

        # 1. GAMMA VETO: If Gamma vetoes, NO TRADE regardless of Alpha and Beta
        if gamma_res.get("veto"):
            action = "HOLD"
            final_score = gamma_res["score"]
            disagreement = 0.0
            gamma_vetoed = True
            reason = "GAMMA_VETO"
        else:
            gamma_vetoed = False
            # 2. Weighted Consensus
            final_score = round(
                (alpha_res["score"] * self.alpha.WEIGHT)
                + (beta_res["score"] * self.beta.WEIGHT)
                + (gamma_res["score"] * self.gamma.WEIGHT),
                2,
            )

            # 3. Inter-agent Disagreement Check
            scores = [alpha_res["score"], beta_res["score"], gamma_res["score"]]
            disagreement = round(statistics.stdev(scores), 2) if len(scores) > 1 else 0.0

            if disagreement > self.MAX_DISAGREEMENT:
                action = "HOLD"
                reason = "HIGH_DISAGREEMENT"
            elif final_score >= self.TRADE_THRESHOLD:
                action = "BUY"
                reason = "CONSENSUS"
            elif final_score <= -self.TRADE_THRESHOLD:
                action = "SELL"
                reason = "CONSENSUS"
            else:
                action = "HOLD"
                reason = "CONSENSUS"

        # 4. Synthesize Strategic Memo via Local LLM (Ollama)
        strategic_memo = local_journal_generator.generate_journal(
            symbol=symbol,
            alpha_score=alpha_res["score"],
            beta_score=beta_res["score"],
            gamma_score=gamma_res["score"],
            gamma_veto=gamma_vetoed,
            action=action,
            final_score=final_score,
        )

        return {
            "symbol": symbol,
            "action": action,
            "reason": reason,
            "final_score": final_score,
            "disagreement": disagreement,
            "gamma_vetoed": gamma_vetoed,
            "alpha": alpha_res,
            "beta": beta_res,
            "gamma": gamma_res,
            "strategic_memo": strategic_memo,
        }


triad_orchestrator = CognitiveTriadOrchestrator()
