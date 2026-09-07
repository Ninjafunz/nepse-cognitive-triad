"use client";

import React from "react";
import { ShieldCheck, Activity, Bell, Search } from "lucide-react";
import { portfolioMetrics } from "@/lib/mockData";

export default function Header() {
  return (
    <header className="h-14 border-b border-zinc-800/80 bg-zinc-950/80 backdrop-blur px-6 flex items-center justify-between shrink-0 sticky top-0 z-40">
      {/* Ticker Search & Quick Info */}
      <div className="flex items-center space-x-4">
        <div className="relative">
          <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" />
          <input
            type="text"
            placeholder="Search symbol (e.g. NABIL, SHIVM)..."
            defaultValue="NABIL"
            className="pl-8 pr-3 py-1.5 bg-zinc-900 border border-zinc-800 rounded-lg text-xs text-zinc-200 placeholder-zinc-500 font-mono focus:outline-none focus:border-zinc-700 w-56"
          />
        </div>

        <div className="hidden md:flex items-center space-x-2 text-xs font-mono text-zinc-400">
          <span className="text-zinc-600">|</span>
          <span>NEPSE Index: <strong className="text-zinc-200">2,085.40</strong></span>
          <span className="text-emerald-400 font-semibold">(+0.60%)</span>
          <span className="text-zinc-600">|</span>
          <span>Turnover: <strong className="text-zinc-200">NPR 4.21B</strong></span>
        </div>
      </div>

      {/* Sovereign Capital & Status Indicators */}
      <div className="flex items-center space-x-5 text-xs font-mono">
        <div className="hidden lg:flex items-center space-x-3 bg-zinc-900/90 border border-zinc-800/80 px-3 py-1.5 rounded-lg">
          <span className="text-zinc-400 font-sans">Settled Buying Power:</span>
          <span className="text-emerald-400 font-bold font-mono">
            NPR {portfolioMetrics.settledCash.toLocaleString("en-US", { minimumFractionDigits: 2 })}
          </span>
        </div>

        <div className="flex items-center space-x-2">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="font-bold text-zinc-300">SESSION OPEN</span>
        </div>

        <button className="p-1.5 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900 rounded-lg border border-transparent hover:border-zinc-800 transition">
          <Bell className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
}
