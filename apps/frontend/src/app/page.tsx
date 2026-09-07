"use client";

import React from "react";
import {
  Wallet,
  TrendingUp,
  Clock,
  ShieldCheck,
  AlertTriangle,
  ArrowUpRight,
  ArrowDownRight,
  ShieldAlert,
  Terminal,
} from "lucide-react";
import {
  portfolioMetrics,
  equityCurveData,
  liveSignalsFeed,
} from "@/lib/mockData";

export default function ExecutiveDashboard() {
  const maxEquity = Math.max(...equityCurveData.map((d) => d.equity));
  const minEquity = Math.min(...equityCurveData.map((d) => d.equity));

  return (
    <div className="space-y-6">
      {/* 1. Top Metric Cards (Institutional Dense) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Portfolio Capital */}
        <div className="bg-zinc-900/90 border border-zinc-800/90 p-4 rounded-xl shadow-lg relative overflow-hidden">
          <div className="flex justify-between items-center text-zinc-400 text-xs">
            <span className="font-medium tracking-wide">TOTAL VIRTUAL CAPITAL</span>
            <Wallet className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-zinc-100 mt-2">
            NPR {portfolioMetrics.totalCapital.toLocaleString("en-US", { minimumFractionDigits: 2 })}
          </div>
          <div className="flex items-center space-x-1.5 mt-2 text-xs font-mono text-emerald-400">
            <ArrowUpRight className="w-3.5 h-3.5" />
            <span>+86.74% Historical Return</span>
          </div>
        </div>

        {/* Settled Cash (T+2 Buying Power) */}
        <div className="bg-zinc-900/90 border border-zinc-800/90 p-4 rounded-xl shadow-lg">
          <div className="flex justify-between items-center text-zinc-400 text-xs">
            <span className="font-medium tracking-wide">SETTLED CASH (BUYING POWER)</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-2">
            NPR {portfolioMetrics.settledCash.toLocaleString("en-US", { minimumFractionDigits: 2 })}
          </div>
          <div className="text-xs text-zinc-500 mt-2 font-mono">
            Immediately spendable under T+2 rule
          </div>
        </div>

        {/* Unsettled Receivables */}
        <div className="bg-zinc-900/90 border border-zinc-800/90 p-4 rounded-xl shadow-lg">
          <div className="flex justify-between items-center text-zinc-400 text-xs">
            <span className="font-medium tracking-wide">UNSETTLED T+2 RECEIVABLES</span>
            <Clock className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-amber-400 mt-2">
            NPR {portfolioMetrics.unsettledCash.toLocaleString("en-US", { minimumFractionDigits: 2 })}
          </div>
          <div className="text-xs text-zinc-500 mt-2 font-mono">
            Settles in 2 NEPSE business days
          </div>
        </div>

        {/* Active System Status */}
        <div className="bg-zinc-900/90 border border-zinc-800/90 p-4 rounded-xl shadow-lg">
          <div className="flex justify-between items-center text-zinc-400 text-xs">
            <span className="font-medium tracking-wide">SYSTEM INTEGRITY</span>
            <ShieldAlert className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-2 flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>{portfolioMetrics.systemStatus}</span>
          </div>
          <div className="text-xs text-zinc-500 mt-2 font-mono">
            Taleb Veto Guard Armed & Nominal
          </div>
        </div>
      </div>

      {/* 2. Middle Row (Equity Curve Chart + Active Signals Feed) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left (65%): Equity Growth Curve */}
        <div className="lg:col-span-8 bg-zinc-900/90 border border-zinc-800/90 rounded-xl p-5 shadow-lg space-y-4">
          <div className="flex justify-between items-center border-b border-zinc-800/80 pb-3">
            <div>
              <h2 className="text-sm font-bold text-zinc-100 tracking-tight flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-indigo-400" />
                <span>PORTFOLIO EQUITY CURVE (2021 HISTORIC EXPANSION)</span>
              </h2>
              <p className="text-xs text-zinc-400 font-mono mt-0.5">
                NPR 13.30M Initial Capital → NPR 24.84M (+86.74%) vs NEPSE Benchmark
              </p>
            </div>
            <div className="flex items-center space-x-3 text-xs font-mono">
              <span className="flex items-center gap-1 text-indigo-400">
                <span className="w-2 h-2 bg-indigo-500 rounded-full"></span> Triad Portfolio
              </span>
              <span className="flex items-center gap-1 text-zinc-500">
                <span className="w-2 h-2 bg-zinc-600 rounded-full"></span> Buy & Hold
              </span>
            </div>
          </div>

          {/* Styled SVG Chart (Fast, Zero Dependencies) */}
          <div className="h-64 w-full relative pt-2">
            <svg viewBox="0 0 800 240" className="w-full h-full overflow-visible">
              <defs>
                <linearGradient id="equityGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#6366f1" stopOpacity="0.35" />
                  <stop offset="100%" stopColor="#6366f1" stopOpacity="0.0" />
                </linearGradient>
              </defs>

              {/* Grid Lines */}
              {[40, 90, 140, 190].map((y) => (
                <line
                  key={y}
                  x1="40"
                  y1={y}
                  x2="780"
                  y2={y}
                  stroke="#27272a"
                  strokeDasharray="3 3"
                />
              ))}

              {/* Benchmark Curve */}
              <polyline
                fill="none"
                stroke="#52525b"
                strokeWidth="2"
                strokeDasharray="4 4"
                points={equityCurveData
                  .map((d, i) => {
                    const x = 40 + (i * (740 / (equityCurveData.length - 1)));
                    const y = 220 - ((d.benchmark - minEquity) / (maxEquity - minEquity) * 190);
                    return `${x},${y}`;
                  })
                  .join(" ")}
              />

              {/* Filled Gradient Area */}
              <polygon
                fill="url(#equityGrad)"
                points={`40,220 ${equityCurveData
                  .map((d, i) => {
                    const x = 40 + (i * (740 / (equityCurveData.length - 1)));
                    const y = 220 - ((d.equity - minEquity) / (maxEquity - minEquity) * 190);
                    return `${x},${y}`;
                  })
                  .join(" ")} 780,220`}
              />

              {/* Triad Portfolio Curve */}
              <polyline
                fill="none"
                stroke="#6366f1"
                strokeWidth="3"
                points={equityCurveData
                  .map((d, i) => {
                    const x = 40 + (i * (740 / (equityCurveData.length - 1)));
                    const y = 220 - ((d.equity - minEquity) / (maxEquity - minEquity) * 190);
                    return `${x},${y}`;
                  })
                  .join(" ")}
              />

              {/* Data Points */}
              {equityCurveData.map((d, i) => {
                const x = 40 + (i * (740 / (equityCurveData.length - 1)));
                const y = 220 - ((d.equity - minEquity) / (maxEquity - minEquity) * 190);
                return (
                  <circle
                    key={i}
                    cx={x}
                    cy={y}
                    r="4"
                    className="fill-indigo-400 stroke-zinc-950 stroke-2 hover:r-6 transition-all"
                  />
                );
              })}
            </svg>
          </div>

          <div className="flex justify-between text-[11px] font-mono text-zinc-500 pt-1">
            {equityCurveData.map((d, i) => (
              <span key={i}>{d.time}</span>
            ))}
          </div>
        </div>

        {/* Right (35%): Live Signals Feed */}
        <div className="lg:col-span-4 bg-zinc-900/90 border border-zinc-800/90 rounded-xl p-5 shadow-lg space-y-3 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-zinc-800/80 pb-3 mb-3">
              <h2 className="text-sm font-bold text-zinc-100 tracking-tight flex items-center gap-2">
                <Terminal className="w-4 h-4 text-cyan-400" />
                <span>DECISION FEED</span>
              </h2>
              <span className="text-[10px] font-mono bg-zinc-800 text-zinc-400 px-2 py-0.5 rounded border border-zinc-700">
                LIVE AUDIT
              </span>
            </div>

            <div className="space-y-2.5">
              {liveSignalsFeed.map((item) => {
                const badgeColor =
                  item.badgeType === "danger"
                    ? "bg-rose-950/80 text-rose-400 border-rose-800"
                    : item.badgeType === "success"
                    ? "bg-emerald-950/80 text-emerald-400 border-emerald-800"
                    : item.badgeType === "warning"
                    ? "bg-amber-950/80 text-amber-400 border-amber-800"
                    : "bg-blue-950/80 text-blue-400 border-blue-800";

                return (
                  <div
                    key={item.id}
                    className="p-2.5 rounded-lg bg-zinc-950 border border-zinc-800/80 space-y-1 hover:border-zinc-700 transition"
                  >
                    <div className="flex items-center justify-between text-[11px] font-mono">
                      <span className="font-bold text-zinc-200">{item.symbol}</span>
                      <span className="text-zinc-500">{item.time}</span>
                    </div>
                    <p className="text-xs text-zinc-400 leading-relaxed font-sans">
                      {item.message}
                    </p>
                    <div className="flex items-center justify-between pt-1 text-[10px] font-mono">
                      <span className="text-zinc-500">Agent: {item.agent}</span>
                      <span className={`px-1.5 py-0.2 rounded border font-bold ${badgeColor}`}>
                        {item.action}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="pt-2 border-t border-zinc-800 text-[11px] text-zinc-500 font-mono text-center">
            Zero execution leaks • Real-time negative asymmetry filters
          </div>
        </div>
      </div>

      {/* 3. Bottom Row: Strategic Epistemic Thesis */}
      <div className="bg-gradient-to-r from-zinc-900 via-zinc-900 to-indigo-950/40 border border-zinc-800 rounded-xl p-5 shadow-lg">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="space-y-1">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <span>The Cognitive Prosthetic Philosophy</span>
              <span className="text-[10px] font-mono text-indigo-400 bg-indigo-950 border border-indigo-800 px-2 py-0.5 rounded">
                Strategic Governance
              </span>
            </h3>
            <p className="text-xs text-zinc-400 max-w-4xl leading-relaxed">
              *"Just as an astronomer does not surrender cognitive sovereignty to the telescope, a strategist must never abdicate governance to an uninterpretable machine learning model. The telescope sharpens perception; the astronomer defines the questions and governs the cosmos."*
            </p>
          </div>
          <a
            href="/consciousness"
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-mono font-semibold transition shrink-0 shadow-lg shadow-indigo-950/60"
          >
            Inspect Triad Debate →
          </a>
        </div>
      </div>
    </div>
  );
}
