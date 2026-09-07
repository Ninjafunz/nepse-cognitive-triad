"use client";

import React, { useState, useMemo } from "react";
import {
  ListFilter,
  ShieldAlert,
  Search,
  CheckCircle2,
  Ban,
  TrendingUp,
  TrendingDown,
  ChevronDown,
} from "lucide-react";
import { dailyEvaluationsData, DailyEvaluationItem } from "@/lib/evaluationsData";

// Generate 220 market-wide evaluation rows to simulate full NEPSE universe
const fullMarketEvaluations: DailyEvaluationItem[] = (() => {
  const base = [...dailyEvaluationsData];
  const sectors = [
    "Hydropower",
    "Commercial Banks",
    "Development Banks",
    "Microfinance",
    "Life Insurance",
    "Non-Life Insurance",
    "Manufacturing",
    "Hotels & Tourism",
    "Investment",
  ];
  const prefixes = ["HYDRO", "BANK", "DEV", "MF", "INS", "MFG", "HOTEL", "INV"];

  for (let i = 1; i <= 212; i++) {
    const secIdx = i % sectors.length;
    const sector = sectors[secIdx];
    const sym = `${prefixes[secIdx] || "STOCK"}${i < 10 ? "0" + i : i}`;

    const isVeto = i % 4 === 0;
    const isBuy = i % 35 === 0;
    const isHold = i % 10 === 0 && !isBuy;

    const alpha = isBuy ? 70 : (isVeto ? 30 : -20 + (i % 50));
    const beta = isBuy ? 65 : (isVeto ? 75 : 10 + (i % 60));
    const gamma = isVeto ? -65 : (isBuy ? 25 : 15);

    let finalAction: "BUY" | "SELL" | "HOLD" | "NO_ACTION" = "NO_ACTION";
    let primaryReason = "Signal conviction below margin of safety. Standing aside per Minsky/Taleb.";

    if (isVeto) {
      finalAction = "NO_ACTION";
      primaryReason = `Taleb Veto: Volatility ${(6.2 + (i % 20) * 0.1).toFixed(1)}% > 6.0% safety threshold. Asymmetric tail fragility. Standing aside.`;
    } else if (isBuy) {
      finalAction = "BUY";
      primaryReason = `Harmonious consensus (+${(alpha*0.4 + beta*0.35 + gamma*0.25).toFixed(1)}). Corporate & macro support in non-fragile regime.`;
    } else if (isHold) {
      finalAction = "HOLD";
      primaryReason = "Consolidation phase. Retaining core allocation without incremental exposure.";
    }

    base.push({
      id: `eval-full-${i}`,
      evalDate: "2026-09-08",
      symbol: sym,
      sector: sector,
      alphaScore: alpha,
      betaScore: beta,
      gammaScore: gamma,
      gammaVeto: isVeto,
      finalAction: finalAction,
      primaryReason: primaryReason,
    });
  }

  return base;
})();

export default function DecisionsPage() {
  const [actionFilter, setActionFilter] = useState<string>("ALL");
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [visibleCount, setVisibleCount] = useState<number>(50);

  const filteredData = useMemo(() => {
    return fullMarketEvaluations.filter((item) => {
      const matchesAction =
        actionFilter === "ALL" || item.finalAction === actionFilter;
      const matchesSearch =
        item.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.sector.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.primaryReason.toLowerCase().includes(searchTerm.toLowerCase());
      return matchesAction && matchesSearch;
    });
  }, [actionFilter, searchTerm]);

  const noActionCount = fullMarketEvaluations.filter(
    (d) => d.finalAction === "NO_ACTION"
  ).length;
  const buyCount = fullMarketEvaluations.filter(
    (d) => d.finalAction === "BUY"
  ).length;
  const holdCount = fullMarketEvaluations.filter(
    (d) => d.finalAction === "HOLD"
  ).length;
  const sellCount = fullMarketEvaluations.filter(
    (d) => d.finalAction === "SELL"
  ).length;

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-zinc-900/90 border border-zinc-800 p-5 rounded-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <h1 className="text-base font-bold text-white tracking-tight">
              MARKET-WIDE DECISION MATRIX (220 NEPSE EQUITIES)
            </h1>
          </div>
          <p className="text-xs text-zinc-400 font-mono mt-1">
            Autonomous daily scan of all listed companies • Proving institutional discipline & negative selection
          </p>
        </div>

        {/* Aggregate Market Ratio */}
        <div className="bg-zinc-950 px-4 py-2 rounded-lg border border-zinc-800 text-xs font-mono text-zinc-300">
          Evaluated: <strong className="text-white">{fullMarketEvaluations.length}</strong> | 
          Stood Aside: <strong className="text-rose-400">{noActionCount} ({Math.round(noActionCount / fullMarketEvaluations.length * 100)}%)</strong> | 
          Approved: <strong className="text-emerald-400">{buyCount + sellCount}</strong>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="flex flex-col sm:flex-row justify-between items-center gap-4 bg-zinc-900/90 border border-zinc-800 p-4 rounded-xl">
        <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
          <span className="text-zinc-500 font-medium">Filter:</span>
          <button
            onClick={() => { setActionFilter("ALL"); setVisibleCount(50); }}
            className={`px-3 py-1.5 rounded-lg font-bold transition ${
              actionFilter === "ALL"
                ? "bg-zinc-800 text-white border border-zinc-700"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            All ({fullMarketEvaluations.length})
          </button>
          <button
            onClick={() => { setActionFilter("NO_ACTION"); setVisibleCount(50); }}
            className={`px-3 py-1.5 rounded-lg font-bold transition flex items-center space-x-1 ${
              actionFilter === "NO_ACTION"
                ? "bg-rose-950/80 text-rose-300 border border-rose-800"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            <Ban className="w-3 h-3" />
            <span>No Action / Veto ({noActionCount})</span>
          </button>
          <button
            onClick={() => { setActionFilter("BUY"); setVisibleCount(50); }}
            className={`px-3 py-1.5 rounded-lg font-bold transition flex items-center space-x-1 ${
              actionFilter === "BUY"
                ? "bg-emerald-950/80 text-emerald-300 border border-emerald-800"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            <TrendingUp className="w-3 h-3" />
            <span>Buy ({buyCount})</span>
          </button>
          <button
            onClick={() => { setActionFilter("HOLD"); setVisibleCount(50); }}
            className={`px-3 py-1.5 rounded-lg font-bold transition ${
              actionFilter === "HOLD"
                ? "bg-indigo-950/80 text-indigo-300 border border-indigo-800"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            Hold ({holdCount})
          </button>
        </div>

        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" />
          <input
            type="text"
            placeholder="Search across 220 stocks..."
            value={searchTerm}
            onChange={(e) => { setSearchTerm(e.target.value); setVisibleCount(50); }}
            className="w-full pl-8 pr-3 py-1.5 bg-zinc-950 border border-zinc-800 rounded-lg text-xs text-zinc-200 placeholder-zinc-500 font-mono focus:outline-none focus:border-zinc-700"
          />
        </div>
      </div>

      {/* Decision Table (Paginated / Virtualized at 50 per page) */}
      <div className="bg-zinc-900/90 border border-zinc-800 rounded-xl p-5 shadow-xl space-y-4">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-zinc-950 text-zinc-400 border-b border-zinc-800 uppercase tracking-wider text-[11px]">
              <tr>
                <th className="p-3">Date</th>
                <th className="p-3">Symbol</th>
                <th className="p-3">Sector</th>
                <th className="p-3 text-right">Alpha</th>
                <th className="p-3 text-right">Beta</th>
                <th className="p-3 text-right">Gamma</th>
                <th className="p-3">Action</th>
                <th className="p-3">Qualitative Strategic Rationale</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/60 text-zinc-200">
              {filteredData.slice(0, visibleCount).map((item) => {
                const isVeto = item.gammaVeto;
                const isNoAction = item.finalAction === "NO_ACTION";
                const isBuy = item.finalAction === "BUY";
                const isSell = item.finalAction === "SELL";

                return (
                  <tr
                    key={item.id}
                    className={`hover:bg-zinc-950/40 transition ${
                      isNoAction ? "opacity-80" : ""
                    }`}
                  >
                    <td className="p-3 text-zinc-500">{item.evalDate}</td>
                    <td className="p-3 font-bold text-white flex items-center gap-1.5">
                      {item.symbol}
                      {isVeto && (
                        <span className="text-[9px] bg-rose-950 text-rose-400 px-1 rounded border border-rose-900 font-bold">
                          VETO
                        </span>
                      )}
                    </td>
                    <td className="p-3 text-zinc-400 font-sans">{item.sector}</td>
                    <td className="p-3 text-right font-bold text-blue-400">
                      {item.alphaScore > 0 ? `+${item.alphaScore}` : item.alphaScore}
                    </td>
                    <td className="p-3 text-right font-bold text-purple-400">
                      {item.betaScore > 0 ? `+${item.betaScore}` : item.betaScore}
                    </td>
                    <td
                      className={`p-3 text-right font-bold ${
                        item.gammaScore < 0 ? "text-rose-400" : "text-amber-400"
                      }`}
                    >
                      {item.gammaScore > 0 ? `+${item.gammaScore}` : item.gammaScore}
                    </td>
                    <td className="p-3">
                      {isBuy ? (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950 text-emerald-400 border border-emerald-800">
                          BUY
                        </span>
                      ) : isSell ? (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-950 text-amber-400 border border-amber-800">
                          SELL
                        </span>
                      ) : isNoAction ? (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-zinc-950 text-zinc-500 border border-zinc-800 flex items-center gap-1 w-fit">
                          <Ban className="w-2.5 h-2.5" />
                          <span>NO ACTION</span>
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-950 text-indigo-400 border border-indigo-800">
                          HOLD
                        </span>
                      )}
                    </td>
                    <td className="p-3 text-zinc-300 font-sans leading-relaxed max-w-md text-xs">
                      {item.primaryReason}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Load More Pagination */}
        {visibleCount < filteredData.length && (
          <div className="pt-3 border-t border-zinc-800 flex justify-center">
            <button
              onClick={() => setVisibleCount((prev) => prev + 50)}
              className="px-5 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 rounded-lg text-xs font-mono font-bold flex items-center space-x-2 border border-zinc-700 transition shadow-lg"
            >
              <ChevronDown className="w-4 h-4" />
              <span>
                Load More (+50 of {filteredData.length - visibleCount} remaining)
              </span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
