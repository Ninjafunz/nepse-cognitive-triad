"use client";

import React from "react";
import {
  Layers,
  Wallet,
  Clock,
  CheckCircle2,
  AlertCircle,
  ArrowDownLeft,
  ArrowUpRight,
  ShieldCheck,
} from "lucide-react";
import {
  portfolioMetrics,
  openPositions,
  settlementLedger,
} from "@/lib/mockData";

export default function PortfolioPage() {
  return (
    <div className="space-y-6">
      {/* Capital Summary Header */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-zinc-900/90 border border-zinc-800 p-4 rounded-xl">
          <div className="text-xs text-zinc-400 font-mono">SETTLED SPENDABLE CASH</div>
          <div className="text-xl font-bold font-mono text-emerald-400 mt-1">
            NPR {portfolioMetrics.settledCash.toLocaleString("en-US", { minimumFractionDigits: 2 })}
          </div>
          <div className="text-[11px] text-zinc-500 mt-1">
            Available for immediate order execution
          </div>
        </div>

        <div className="bg-zinc-900/90 border border-zinc-800 p-4 rounded-xl">
          <div className="text-xs text-zinc-400 font-mono">UNSETTLED T+2 RECEIVABLES</div>
          <div className="text-xl font-bold font-mono text-amber-400 mt-1">
            NPR {portfolioMetrics.unsettledCash.toLocaleString("en-US", { minimumFractionDigits: 2 })}
          </div>
          <div className="text-[11px] text-zinc-500 mt-1">
            Excluded from buying power until clearance
          </div>
        </div>

        <div className="bg-zinc-900/90 border border-zinc-800 p-4 rounded-xl">
          <div className="text-xs text-zinc-400 font-mono">TOTAL ACCRUED UNREALIZED PnL</div>
          <div className="text-xl font-bold font-mono text-indigo-400 mt-1">
            +NPR {portfolioMetrics.unrealizedPnL.toLocaleString("en-US", { minimumFractionDigits: 2 })}
          </div>
          <div className="text-[11px] text-emerald-400 font-mono mt-1">
            +27.4% on active deployed positions
          </div>
        </div>
      </div>

      {/* 1. Open Positions Table */}
      <div className="bg-zinc-900/90 border border-zinc-800 rounded-xl p-5 shadow-lg space-y-4">
        <div className="flex justify-between items-center border-b border-zinc-800 pb-3">
          <div className="flex items-center space-x-2">
            <Layers className="w-4 h-4 text-indigo-400" />
            <h2 className="text-sm font-bold text-white tracking-wide">
              OPEN VIRTUAL HOLDINGS
            </h2>
          </div>
          <span className="text-xs font-mono text-zinc-400">
            {openPositions.length} Active Positions • Strict Long-Only (No Shorting)
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-zinc-950 text-zinc-400 border-b border-zinc-800 uppercase tracking-wider text-[11px]">
              <tr>
                <th className="p-3">Symbol</th>
                <th className="p-3">Sector</th>
                <th className="p-3 text-right">Quantity</th>
                <th className="p-3 text-right">Avg Cost (NPR)</th>
                <th className="p-3 text-right">LTP (NPR)</th>
                <th className="p-3 text-right">Unrealized PnL</th>
                <th className="p-3 text-right">Return %</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/60 text-zinc-200">
              {openPositions.map((p) => (
                <tr key={p.symbol} className="hover:bg-zinc-950/50 transition">
                  <td className="p-3 font-bold text-white">{p.symbol}</td>
                  <td className="p-3 text-zinc-400 font-sans">{p.sector}</td>
                  <td className="p-3 text-right font-bold">{p.qty.toLocaleString()}</td>
                  <td className="p-3 text-right text-zinc-400">{p.avgPrice.toFixed(2)}</td>
                  <td className="p-3 text-right font-bold text-white">{p.ltp.toFixed(2)}</td>
                  <td className="p-3 text-right font-bold text-emerald-400">
                    +{p.unrealizedPnL.toLocaleString("en-US", { minimumFractionDigits: 2 })}
                  </td>
                  <td className="p-3 text-right font-bold text-emerald-400">
                    +{p.pnlPct.toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 2. T+2 Settlement Ledger Audit Table */}
      <div className="bg-zinc-900/90 border border-zinc-800 rounded-xl p-5 shadow-lg space-y-4">
        <div className="flex justify-between items-center border-b border-zinc-800 pb-3">
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4 text-emerald-400" />
            <h2 className="text-sm font-bold text-white tracking-wide">
              T+2 SETTLEMENT AUDIT LEDGER
            </h2>
          </div>
          <span className="text-xs font-mono text-zinc-400">
            Immutable Cashflow Engine • NEPSE Working Calendar
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-zinc-950 text-zinc-400 border-b border-zinc-800 uppercase tracking-wider text-[11px]">
              <tr>
                <th className="p-3">Tx ID</th>
                <th className="p-3">Trade Date</th>
                <th className="p-3">Type</th>
                <th className="p-3">Symbol</th>
                <th className="p-3 text-right">Amount (NPR)</th>
                <th className="p-3">Settlement Date</th>
                <th className="p-3">Status</th>
                <th className="p-3">Description</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/60 text-zinc-200">
              {settlementLedger.map((item) => (
                <tr key={item.id} className="hover:bg-zinc-950/50 transition">
                  <td className="p-3 text-zinc-500 font-bold">{item.id}</td>
                  <td className="p-3 text-zinc-400">{item.date}</td>
                  <td className="p-3 font-bold">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] ${
                        item.type === "BUY"
                          ? "bg-blue-950 text-blue-400 border border-blue-900"
                          : item.type === "SELL"
                          ? "bg-amber-950 text-amber-400 border border-amber-900"
                          : "bg-emerald-950 text-emerald-400 border border-emerald-900"
                      }`}
                    >
                      {item.type}
                    </span>
                  </td>
                  <td className="p-3 font-bold text-white">{item.symbol}</td>
                  <td
                    className={`p-3 text-right font-bold ${
                      item.amount >= 0 ? "text-emerald-400" : "text-zinc-300"
                    }`}
                  >
                    {item.amount >= 0 ? "+" : ""}
                    {item.amount.toLocaleString("en-US", { minimumFractionDigits: 2 })}
                  </td>
                  <td className="p-3 text-zinc-400">{item.settledDate}</td>
                  <td className="p-3">
                    {item.status === "SETTLED" ? (
                      <span className="flex items-center space-x-1 text-emerald-400 text-[11px]">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>Settled</span>
                      </span>
                    ) : (
                      <span className="flex items-center space-x-1 text-amber-400 text-[11px] animate-pulse">
                        <Clock className="w-3.5 h-3.5" />
                        <span>Pending T+2</span>
                      </span>
                    )}
                  </td>
                  <td className="p-3 text-zinc-400 font-sans max-w-xs truncate">
                    {item.description}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
