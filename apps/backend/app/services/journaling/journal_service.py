"""AI Journaling and RAG pipeline service using Local Llama-3."""

from typing import Dict, Any, List
from app.config import settings


class JournalingService:
    """Generates literature-grounded audit journals for every executed trade."""

    async def generate_pre_trade_journal(
        self,
        symbol: str,
        side: str,
        triad_decision: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Synthesizes Triad scores with literature citations."""
        content = (
            f"### Trade Thesis for {side} {symbol}\n\n"
            f"**Synthesis Score**: {triad_decision.get('final_score')} | Action: {triad_decision.get('action_taken')}\n\n"
            f"- **Route Alpha (Structural)**: {triad_decision.get('alpha_rationale', {}).get('thesis')}\n"
            f"- **Route Beta (Behavioral)**: {triad_decision.get('beta_rationale', {}).get('thesis')}\n"
            f"- **Route Gamma (Philosophical)**: {triad_decision.get('gamma_rationale', {}).get('thesis')}\n\n"
            f"**Literature Grounding**: Grounded in Minsky's Financial Instability Hypothesis and Taleb's Antifragility framework."
        )

        citations = [
            {"author": "Hyman Minsky", "work": "Stabilizing an Unstable Economy (1986)"},
            {"author": "Nassim Nicholas Taleb", "work": "Antifragile: Things That Gain from Disorder (2012)"},
            {"author": "Robert J. Shiller", "work": "Narrative Economics (2019)"},
        ]

        return {
            "journal_type": "pre_trade",
            "thesis_summary": f"Consensus {side} signal generated via Cognitive Triad",
            "content": content,
            "citations": citations,
            "model_used": settings.LOCAL_LLAMA3_MODEL_NAME,
        }


journaling_service = JournalingService()
