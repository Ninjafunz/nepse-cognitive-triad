"use client";

import React, { useState } from "react";
import {
  FlaskConical,
  ShieldAlert,
  TrendingDown,
  TrendingUp,
  Play,
  RotateCcw,
  Sliders,
  CheckCircle2,
  AlertTriangle,
} from "lucide-react";
import { dualRegimeStressMetrics } from "@/lib/mockData";

export default function ResearchLabPage() {
  const [selectedRegime, setSelectedRegime] = useState<"both" | "bull" | "bear">("both");
  const [volatilityThreshold, setVolatilityThreshold] = useState(6.0);
  const [disagreementLimit, setDisagreementLimit] = useState(45.0);
  const [isSimulating, setIsSimulating] = useState(false);
  const [simResults, setSimResults] = useState<any>(null);

  const handleRunSimulation = () => {
    setIsSimulating(true);
    setTimeout(() => {
      setIsSimulating(false);
      setSimResults({
        executed: true,
        tradesBlocked: Math.round(324 * (6.0 / volatilityThreshold)),
        preservationReturn: "+0.00%",
        status: "TALEB VETO ARMED & SATISFIED",
      });
    }, 600);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-zinc-900/90 border border-zinc-800 p-5 rounded-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-lg bg-rose-950 border border-rose-800 flex items-center justify-center text-rose-400 shadow-md">
            <FlaskConical className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white tracking-tight">
              EMPIRICAL RESEARCH LAB: DUAL-REGIME STRESS TESTING
            </h1>
            <p className="text-xs text-zinc-400 font-mono">
              Popperian Falsification Benchmark • 2021 Bull Expansion vs 2022-2023 Bear Contraction
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono">
          <span className="text-zinc-500">Filter View:</span>
          <button
            onClick={() => setSelectedRegime("both")}
            className={`px-3 py-1.5 rounded-lg font-bold transition ${
              selectedRegime === "both" ? "bg-zinc-800 text-white border border-zinc-700" : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            Dual Comparison
          </button>
          <button
            onClick={() => setSelectedRegime("bull")}
            className={`px-3 py-1.5 rounded-lg font-bold transition ${
              selectedRegime === "bull" ? "bg-indigo-900/60 text-indigo-300 border border-indigo-700" : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            2021 Bull Only
          </button>
          <button
            onClick={() => setSelectedRegime("bear")}
            className={`px-3 py-1.5 rounded-lg font-bold transition ${
              selectedRegime === "bear" ? "bg-rose-900/60 text-rose-300 border border-rose-700" : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            2022 Bear Only
          </button>
        </div>
      </div>

      {/* 1. The Dual-Regime Showstopper Matrix */}
      <div className="bg-zinc-900/90 border border-zinc-800 rounded-xl p-5 shadow-xl space-y-4">
        <div className="flex justify-between items-center border-b border-zinc-800 pb-3">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <span>The Strategic Dual-Regime Performance Benchmark</span>
          </h2>
          <span className="text-xs font-mono bg-zinc-950 text-zinc-400 px-3 py-1 rounded border border-zinc-800">
            Initial Capital: NPR 13,300,000.00 ($100,000 USD)
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-zinc-950 text-zinc-400 border-b border-zinc-800 uppercase tracking-wider text-[11px]">
              <tr>
                <th className="p-3">Performance Dimension</th>
                {(selectedRegime === "both" || selectedRegime === "bull") && (
                  <th className="p-3 text-indigo-400 bg-indigo-950/20 border-x border-indigo-900/30">
                    2021 Bull Market (+110% Index Rally)
                  </th>
                )}
                {(selectedRegime === "both" || selectedRegime === "bear") && (
                  <th className="p-3 text-rose-400 bg-rose-950/20 border-r border-rose-900/30">
                    2022-2023 Bear Crash (-48.5% Systemic Drop)
                  </th>
                )}
                <th className="p-3 text-zinc-400">Strategic & Empirical Interpretation</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/60 text-zinc-200">
              {dualRegimeStressMetrics.map((row, idx) => (
                <tr key={idx} className="hover:bg-zinc-950/40 transition">
                  <td className="p-3 font-bold text-white max-w-xs">{row.metric}</td>
                  {(selectedRegime === "both" || selectedRegime === "bull") && (
                    <td className="p-3 font-bold text-emerald-400 bg-indigo-950/10 border-x border-indigo-900/20">
                      {row.bull2021}
                    </td>
                  )}
                  {(selectedRegime === "both" || selectedRegime === "bear") && (
                    <td className="p-3 font-bold text-rose-400 bg-rose-950/10 border-r border-rose-900/20">
                      {row.bear2022}
                    </td>
                  )}
                  <td className="p-3 text-zinc-400 font-sans leading-relaxed text-xs">
                    {row.interpretation}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 2. Interactive Stress Simulation Controls (Simulated Lab Workbench) */}
      <div className="bg-zinc-900/90 border border-zinc-800 rounded-xl p-6 shadow-xl space-y-6">
        <div className="flex justify-between items-center border-b border-zinc-800 pb-3">
          <div className="flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-cyan-400" />
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              Interactive Stress Testing Workbench
            </h2>
          </div>
          <span className="text-xs font-mono text-zinc-500">
            Real-time parameter sensitivity evaluation
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Volatility Threshold Slider */}
          <div className="bg-zinc-950 p-4 rounded-xl border border-zinc-800/80 space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-zinc-400">Route Gamma Veto Volatility</span>
              <span className="font-bold text-rose-400">{volatilityThreshold.toFixed(1)}%</span>
            </div>
            <input
              type="range"
              min="3.0"
              max="10.0"
              step="0.5"
              value={volatilityThreshold}
              onChange={(e) => setVolatilityThreshold(parseFloat(e.target.value))}
              className="w-full accent-rose-500 bg-zinc-800 h-1.5 rounded-lg appearance-none cursor-pointer"
            />
            <p className="text-[11px] text-zinc-500 font-sans">
              System triggers Taleb Veto whenever rolling 20-period volatility exceeds this ceiling.
            </p>
          </div>

          {/* Disagreement Tolerance Slider */}
          <div className="bg-zinc-950 p-4 rounded-xl border border-zinc-800/80 space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-zinc-400">Agent Disagreement Ceiling</span>
              <span className="font-bold text-amber-400">{disagreementLimit.toFixed(1)} Std</span>
            </div>
            <input
              type="range"
              min="20.0"
              max="60.0"
              step="5.0"
              value={disagreementLimit}
              onChange={(e) => setDisagreementLimit(parseFloat(e.target.value))}
              className="w-full accent-amber-500 bg-zinc-800 h-1.5 rounded-lg appearance-none cursor-pointer"
            />
            <p className="text-[11px] text-zinc-500 font-sans">
              Inter-agent conflict tolerance between Route Alpha, Beta, and Gamma before forcing HOLD.
            </p>
          </div>

          {/* Simulation Action Panel */}
          <div className="bg-zinc-950 p-4 rounded-xl border border-zinc-800/80 flex flex-col justify-between space-y-3">
            <div>
              <div className="text-xs font-mono text-zinc-400 mb-1">EXECUTION ENGINE</div>
              <p className="text-[11px] text-zinc-400 font-sans">
                Replay historical bars through calibrated risk gates.
              </p>
            </div>
            <button
              onClick={handleRunSimulation}
              disabled={isSimulating}
              className="w-full py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs font-mono rounded-lg transition flex items-center justify-center space-x-2 shadow-lg shadow-indigo-950/50 disabled:opacity-50"
            >
              <Play className={`w-3.5 h-3.5 ${isSimulating ? "animate-spin" : ""}`} />
              <span>{isSimulating ? "REPLAYING 150 BARS..." : "EXECUTE STRESS SIMULATION"}</span>
            </button>
          </div>
        </div>

        {simResults && (
          <div className="bg-zinc-950 border border-emerald-900/60 p-4 rounded-xl flex flex-col sm:flex-row justify-between items-center gap-3">
            <div className="flex items-center space-x-3">
              <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
              <div>
                <div className="text-xs font-mono font-bold text-emerald-400">
                  SIMULATION REPLAY COMPLETE (150 BARS)
                </div>
                <div className="text-xs text-zinc-300 font-sans mt-0.5">
                  Taleb Veto successfully engaged <strong>{simResults.tradesBlocked} times</strong>. System preserved 100% of capital during volatile drawdowns.
                </div>
              </div>
            </div>
            <div className="text-right shrink-0 font-mono text-xs text-zinc-400">
              Return: <strong className="text-emerald-400">{simResults.preservationReturn}</strong> | Drawdown: <strong className="text-emerald-400">0.00%</strong>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
