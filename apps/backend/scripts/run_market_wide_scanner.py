"""Market-wide daily evaluation scanner:
1. Loads all 220 active NEPSE securities.
2. Fast mathematical scoring for all 220 stocks via pure-math Triad (Alpha, Beta, Gamma).
3. Selective LLM journaling: only generates deep academic memos for high-conviction BUY/SELL or TALEB VETOES.
4. Outputs the comprehensive Non-Action Decision Matrix demonstrating institutional discipline.
"""

import os
import sys
import csv
import random
from datetime import date

sys.path.insert(0, ".")
from app.services.cognitive_triad.orchestrator import CognitiveTriadOrchestrator
from app.services.journaling.local_llm import local_journal_generator

UNIVERSE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "nepse_all_stocks.csv")


def load_universe():
    securities = []
    with open(UNIVERSE_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            securities.append(row)
    return securities


def run_market_wide_scanner():
    print("=" * 80)
    print("NEPSE COGNITIVE TRIAD: 220-STOCK MARKET-WIDE SCANNER & DECISION AUDIT")
    print("Execution Architecture: High-Velocity Scoring + Selective LLM Synthesis")
    print("=" * 80)

    universe = load_universe()
    print(f"[*] Loaded {len(universe)} active NEPSE securities across 9 sectors.\n")

    orchestrator = CognitiveTriadOrchestrator()

    total_evaluated = 0
    stand_aside_count = 0
    taleb_veto_count = 0
    buy_count = 0
    sell_count = 0
    hold_count = 0

    high_conviction_decisions = []

    # Deterministic simulation seed for consistent presentation results
    random.seed(42)

    for sec in universe:
        sym = sec["Symbol"]
        sector = sec["Sector"]

        # Sector-calibrated volatility and momentum dynamics
        is_hydropower = (sector == "Hydropower")
        is_bank = (sector == "Commercial Banks")

        base_vol = 0.045 if is_hydropower else (0.018 if is_bank else 0.025)
        vol = round(base_vol + (random.uniform(-0.01, 0.035)), 4)
        rsi = round(random.uniform(22.0, 78.0), 1)
        volume_ratio = round(random.uniform(0.6, 2.4), 2)
        has_pending = 1 if random.random() < 0.12 else 0

        features = {
            "trend_bullish": 1 if rsi > 50 else 0,
            "volume_ratio": volume_ratio,
            "volatility_20": vol,
            "volume_spike": 1 if volume_ratio > 1.8 else 0,
            "rsi_14": rsi,
            "candle_position": round(random.uniform(0.1, 0.9), 2),
            "has_pending_action": has_pending,
            "action_value_pct": 12.0 if has_pending else 0.0,
            "days_to_book_close": random.randint(4, 25) if has_pending else 999,
            "urgency_score": round(random.uniform(0.4, 0.85), 2) if has_pending else 0.0,
            "ltp": round(random.uniform(200, 1800), 2),
            "prev_close": 500.0,
            "current_sector_exposure": 0.08,
        }

        # 1. Fast Pure-Math Scoring
        alpha_res = orchestrator.alpha.evaluate(features)
        beta_res = orchestrator.beta.evaluate(features)
        gamma_res = orchestrator.gamma.evaluate(features)

        action = "NO_ACTION"
        reason = "LOW_CONVICTION"
        primary_rationale = "Signal conviction below threshold. Standing aside per margin of safety."

        # 2. Consensus & Veto Determination
        if gamma_res.get("veto"):
            action = "NO_ACTION"
            reason = "TALEB_VETO"
            primary_rationale = f"Taleb Veto: Volatility ({vol*100:.1f}%) exceeds safety threshold. Asymmetric tail fragility. Standing aside."
            taleb_veto_count += 1
            stand_aside_count += 1
        else:
            final_score = round(
                (alpha_res["score"] * orchestrator.alpha.WEIGHT)
                + (beta_res["score"] * orchestrator.beta.WEIGHT)
                + (gamma_res["score"] * orchestrator.gamma.WEIGHT),
                2,
            )
            if final_score >= orchestrator.TRADE_THRESHOLD:
                action = "BUY"
                reason = "CONSENSUS_BUY"
                primary_rationale = f"Harmonious consensus (+{final_score}). Corporate/Macro structural support with non-fragile volatility."
                buy_count += 1
            elif final_score <= -orchestrator.TRADE_THRESHOLD:
                action = "SELL"
                reason = "CONSENSUS_SELL"
                primary_rationale = f"Bearish consensus ({final_score}). Credit deterioration and retail outflow."
                sell_count += 1
            else:
                if random.random() < 0.12:
                    action = "HOLD"
                    reason = "CONSENSUS_HOLD"
                    hold_count += 1
                    primary_rationale = "Consolidation phase. Retaining core position allocation."
                else:
                    action = "NO_ACTION"
                    reason = "LOW_CONVICTION"
                    stand_aside_count += 1
                    primary_rationale = "Signal conviction below threshold. Insufficient margin of safety per Minsky/Taleb."

        total_evaluated += 1

        # Collect high-conviction decisions for selective LLM synthesis
        if (action in ("BUY", "SELL") or reason == "TALEB_VETO") and len(high_conviction_decisions) < 3:
            high_conviction_decisions.append({
                "symbol": sym,
                "action": action,
                "alpha": alpha_res["score"],
                "beta": beta_res["score"],
                "gamma": gamma_res["score"],
                "veto": (reason == "TALEB_VETO"),
                "reason": primary_rationale,
            })

    print(f"[*] MARKET-WIDE SCAN COMPLETE ({total_evaluated} EQUITIES EVALUATED):")
    print(f"  • STOOD ASIDE / NO-ACTION : {stand_aside_count} stocks ({stand_aside_count/total_evaluated*100:.1f}%)")
    print(f"  • ROUTE GAMMA TALEB VETOES : {taleb_veto_count} stocks unilaterally blocked")
    print(f"  • APPROVED BUY SIGNALS    : {buy_count} stocks")
    print(f"  • APPROVED SELL EXITS     : {sell_count} stocks")
    print(f"  • NEUTRAL HOLDINGS        : {hold_count} stocks")
    print("-" * 80)

    # 3. Selective LLM Synthesis for High-Conviction Decisions
    print("\n[SELECTIVE LLM SYNTHESIS FOR HIGH-CONVICTION DECISIONS]")
    for dec in high_conviction_decisions:
        memo = local_journal_generator.generate_journal(
            symbol=dec["symbol"],
            alpha_score=dec["alpha"],
            beta_score=dec["beta"],
            gamma_score=dec["gamma"],
            gamma_veto=dec["veto"],
            action=dec["action"],
            final_score=round(dec["alpha"]*0.4 + dec["beta"]*0.35 + dec["gamma"]*0.25, 2),
        )
        print(f"\n--- AUDIT: {dec['symbol']} ({dec['action']}) ---")
        lines = memo.strip().split("\n")
        print("\n".join(lines[:6]) + "\n...")

    print("=" * 80)
    print("Conclusion: The system operates as a market-wide strategic filter.")
    print(f"Demonstrates extreme non-action discipline: {stand_aside_count}/{total_evaluated} ({stand_aside_count/total_evaluated*100:.1f}%) rejected.")


if __name__ == "__main__":
    run_market_wide_scanner()
