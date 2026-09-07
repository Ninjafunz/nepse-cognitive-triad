"""Journal Generator using Local Llama-3 (Ollama) with deterministic fallback.
Synthesizes decision context with literature citations into structured trade audit entries.
"""

from typing import Dict, Any, List
import logging
import httpx

try:
    from app.config import settings
    LLAMA3_API_BASE = settings.LOCAL_LLAMA3_API_BASE
    MODEL_NAME = settings.LOCAL_LLAMA3_MODEL_NAME
except Exception:
    LLAMA3_API_BASE = "http://localhost:11434/v1"
    MODEL_NAME = "llama3:70b"

logger = logging.getLogger(__name__)


class JournalGenerator:
    """THE COGNITIVE PROSTHETIC'S VOICE
    The AI drafts the journal citing academic theories; the human strategist audits and retains authority.
    """

    SYSTEM_PROMPT = (
        "You are the journaling module of the NEPSE Cognitive Triad AI Trader. "
        "Your role is NOT to make decisions, but to EXPLAIN decisions already reached "
        "by the three routes (Alpha: Structural Economics, Beta: Behavioral Psychology, Gamma: Philosophical Risk). "
        "Write in the first person as the cognitive system reporting to its human strategist. "
        "Cite specific literature from the context. Acknowledge that the human holds ultimate authority."
    )

    async def generate_journal_entry(
        self,
        symbol: str,
        decision: Dict[str, Any],
        relevant_literature: List[Dict[str, str]] = None,
    ) -> str:
        literature = relevant_literature or [
            {"author": "Hyman Minsky", "citation": "Minsky (1986): Transition into speculative finance phase."},
            {"author": "Robert Shiller", "citation": "Shiller (2019): Viral retail narrative acceleration."},
            {"author": "Nassim Nicholas Taleb", "citation": "Taleb (2012): Fragility constraints & downside asymmetry."},
        ]

        # Prepare context
        lit_context = "\n".join([f"- {item['author']}: {item['citation']}" for item in literature])
        alpha_text = "\n".join([f"  * {r}" for r in decision.get("alpha", {}).get("rationale", [])])
        beta_text = "\n".join([f"  * {r}" for r in decision.get("beta", {}).get("rationale", [])])
        gamma_text = "\n".join([f"  * {r}" for r in decision.get("gamma", {}).get("rationale", [])])

        prompt = (
            f"{self.SYSTEM_PROMPT}\n\n"
            f"=== TRADE DECISION CONTEXT ===\n"
            f"Symbol: {symbol}\n"
            f"Action: {decision.get('action')}\n"
            f"Consensus Score: {decision.get('final_score')}\n"
            f"Disagreement Index: {decision.get('disagreement')}\n"
            f"Gamma Vetoed: {decision.get('gamma_vetoed', False)}\n\n"
            f"Route Alpha (Score: {decision.get('alpha', {}).get('score')}):\n{alpha_text}\n\n"
            f"Route Beta (Score: {decision.get('beta', {}).get('score')}):\n{beta_text}\n\n"
            f"Route Gamma (Score: {decision.get('gamma', {}).get('score')}):\n{gamma_text}\n\n"
            f"=== RETRIEVED ACADEMIC LITERATURE ===\n{lit_context}\n\n"
            f"Provide a structured, literature-grounded audit journal entry:"
        )

        # Attempt call to Local Llama-3 API (Ollama / vLLM OpenAI-compatible endpoint)
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(
                    f"{LLAMA3_API_BASE}/chat/completions",
                    json={
                        "model": MODEL_NAME,
                        "messages": [
                            {"role": "system", "content": self.SYSTEM_PROMPT},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.3,
                        "max_tokens": 800,
                    },
                )
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.info(f"Local Llama-3 endpoint offline ({e}). Generating template-grounded journal synthesis.")

        # Deterministic literature-grounded fallback
        action = decision.get("action")
        return (
            f"### Executive Trade Audit: {action} {symbol}\n\n"
            f"**Synthesis Consensus Score**: {decision.get('final_score')} (Disagreement Std: {decision.get('disagreement')})\n\n"
            f"#### 1. Route Alpha (Structural Economics & Law)\n"
            f"Score: {decision.get('alpha', {}).get('score')}/100\n"
            f"{alpha_text}\n\n"
            f"#### 2. Route Beta (Behavioral Psychology & Narrative)\n"
            f"Score: {decision.get('beta', {}).get('score')}/100\n"
            f"{beta_text}\n\n"
            f"#### 3. Route Gamma (Philosophical Risk & Tail Fragility)\n"
            f"Score: {decision.get('gamma', {}).get('score')}/100 | Veto Status: {decision.get('gamma_vetoed')}\n"
            f"{gamma_text}\n\n"
            f"#### 4. Grounded Literature Citations\n"
            f"{lit_context}\n\n"
            f"--- \n"
            f"*System Note: Generated by the Cognitive Triad AI module as an advisory prosthetic. "
            f"Final strategic authority rests strictly with the human trader.*"
        )


journal_generator = JournalGenerator()
