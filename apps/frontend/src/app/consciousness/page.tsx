"use client";

import React, { useState } from "react";
import {
  Brain,
  ShieldAlert,
  BookOpen,
  TrendingUp,
  AlertTriangle,
  RotateCcw,
  Scale,
  FileText,
  Lock,
} from "lucide-react";
import { triadCurrentState, journalMemoMarkdown } from "@/lib/mockData";

export default function ConsciousnessPage() {
  const [selectedSymbol, setSelectedSymbol] = useState("NABIL");
  const [isSynthesizing, setIsSynthesizing] = useState(false);

  const handleResynthesize = () => {
    setIsSynthesizing(true);
    setTimeout(() => {
      setIsSynthesizing(false);
    }, 600);
  };

  return (
    <div className="space-y-6">
      {/* Header & Symbol Selector */}
      <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4 bg-zinc-900/90 border border-zinc-800 p-5 rounded-xl">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-lg bg-indigo-950 border border-indigo-800 flex items-center justify-center text-indigo-400 shadow-md">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white tracking-tight">
              AI CONSCIOUSNESS & MULTI-AGENT SYNTHESIS
            </h1>
            <p className="text-xs text-zinc-400 font-mono">
              Constitutional Multi-Disciplinary Triad • Taleb Veto Mechanism • RAG Literature Grounding
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {["NABIL", "SHIVM", "CHCL", "HDL"].map((sym) => (
            <button
              key={sym}
              onClick={() => setSelectedSymbol(sym)}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold transition ${
                selectedSymbol === sym
                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-950/60"
                  : "bg-zinc-800 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-700"
              }`}
            >
              {sym}
            </button>
          ))}
          <button
            onClick={handleResynthesize}
            className="p-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-lg border border-zinc-700 transition"
            title="Re-run Multi-Agent Synthesis"
          >
            <RotateCcw className={`w-4 h-4 ${isSynthesizing ? "animate-spin text-indigo-400" : ""}`} />
          </button>
        </div>
      </div>

      {/* 1. The Triad Debate: 3 Agent Cards Side-by-Side */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Route Alpha */}
        <div className="bg-zinc-900/90 border border-blue-900/50 rounded-xl p-5 shadow-lg space-y-3 relative overflow-hidden">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-xs font-mono text-blue-400 font-bold uppercase tracking-wider">
                Route Alpha (40% Weight)
              </span>
              <h2 className="text-sm font-bold text-white mt-0.5">
                The Structural Rationalist
              </h2>
              <p className="text-[11px] text-zinc-400 font-mono">
                {triadCurrentState.alpha.discipline}
              </p>
            </div>
            <div className="text-right">
              <span className="font-mono text-xl font-bold text-blue-400">
                +{triadCurrentState.alpha.score}
              </span>
              <span className="text-[10px] text-zinc-500 font-mono block">/ 100</span>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-zinc-950 h-1.5 rounded-full overflow-hidden">
            <div
              className="bg-blue-500 h-full rounded-full transition-all"
              style={{ width: `${triadCurrentState.alpha.score}%` }}
            ></div>
          </div>

          <div className="space-y-1.5 pt-1 text-xs text-zinc-300 leading-relaxed font-sans">
            {triadCurrentState.alpha.rationale.map((r, i) => (
              <div key={i} className="flex items-start space-x-1.5">
                <span className="text-blue-400 font-mono">•</span>
                <span>{r}</span>
              </div>
            ))}
          </div>

          <div className="pt-2 border-t border-zinc-800/80 flex flex-wrap gap-1.5">
            {triadCurrentState.alpha.citations.map((c, i) => (
              <span
                key={i}
                className="text-[10px] font-mono bg-blue-950/80 text-blue-300 border border-blue-900 px-2 py-0.5 rounded"
              >
                {c}
              </span>
            ))}
          </div>
        </div>

        {/* Route Beta */}
        <div className="bg-zinc-900/90 border border-purple-900/50 rounded-xl p-5 shadow-lg space-y-3 relative overflow-hidden">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-xs font-mono text-purple-400 font-bold uppercase tracking-wider">
                Route Beta (35% Weight)
              </span>
              <h2 className="text-sm font-bold text-white mt-0.5">
                The Behavioral Synthesizer
              </h2>
              <p className="text-[11px] text-zinc-400 font-mono">
                {triadCurrentState.beta.discipline}
              </p>
            </div>
            <div className="text-right">
              <span className="font-mono text-xl font-bold text-purple-400">
                +{triadCurrentState.beta.score}
              </span>
              <span className="text-[10px] text-zinc-500 font-mono block">/ 100</span>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-zinc-950 h-1.5 rounded-full overflow-hidden">
            <div
              className="bg-purple-500 h-full rounded-full transition-all"
              style={{ width: `${triadCurrentState.beta.score}%` }}
            ></div>
          </div>

          <div className="space-y-1.5 pt-1 text-xs text-zinc-300 leading-relaxed font-sans">
            {triadCurrentState.beta.rationale.map((r, i) => (
              <div key={i} className="flex items-start space-x-1.5">
                <span className="text-purple-400 font-mono">•</span>
                <span>{r}</span>
              </div>
            ))}
          </div>

          <div className="pt-2 border-t border-zinc-800/80 flex flex-wrap gap-1.5">
            {triadCurrentState.beta.citations.map((c, i) => (
              <span
                key={i}
                className="text-[10px] font-mono bg-purple-950/80 text-purple-300 border border-purple-900 px-2 py-0.5 rounded"
              >
                {c}
              </span>
            ))}
          </div>
        </div>

        {/* Route Gamma: The Taleb Veto Guard */}
        <div className="bg-zinc-900/90 border-2 border-rose-600 rounded-xl p-5 shadow-xl shadow-rose-950/20 space-y-3 relative overflow-hidden animate-pulse">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-xs font-mono text-rose-400 font-bold uppercase tracking-wider flex items-center gap-1.5">
                <ShieldAlert className="w-3.5 h-3.5" />
                <span>Route Gamma (25% + VETO)</span>
              </span>
              <h2 className="text-sm font-bold text-white mt-0.5">
                The Philosophical Systemist
              </h2>
              <p className="text-[11px] text-zinc-400 font-mono">
                {triadCurrentState.gamma.discipline}
              </p>
            </div>
            <div className="text-right">
              <span className="font-mono text-xl font-bold text-rose-400">
                {triadCurrentState.gamma.score}
              </span>
              <span className="text-[10px] text-rose-500 font-mono font-bold block">
                🛑 VETO
              </span>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-zinc-950 h-1.5 rounded-full overflow-hidden">
            <div className="bg-rose-600 h-full rounded-full w-full"></div>
          </div>

          <div className="space-y-1.5 pt-1 text-xs text-rose-200 leading-relaxed font-sans">
            {triadCurrentState.gamma.rationale.map((r, i) => (
              <div key={i} className="flex items-start space-x-1.5">
                <span className="text-rose-400 font-mono">•</span>
                <span>{r}</span>
              </div>
            ))}
          </div>

          <div className="pt-2 border-t border-rose-900/60 flex flex-wrap gap-1.5">
            {triadCurrentState.gamma.citations.map((c, i) => (
              <span
                key={i}
                className="text-[10px] font-mono bg-rose-950 text-rose-300 border border-rose-800 px-2 py-0.5 rounded"
              >
                {c}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* 2. Middle Section: Consensus Banner */}
      <div className="bg-gradient-to-r from-rose-950/60 via-zinc-900 to-zinc-900 border-2 border-rose-600/80 rounded-xl p-5 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-rose-600 flex items-center justify-center text-white shrink-0 shadow-lg shadow-rose-950/80">
            <Lock className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-rose-900 text-rose-200 border border-rose-700">
                CONSTITUTIONAL VETO OVERRIDE
              </span>
              <span className="text-xs font-mono text-zinc-400">
                Disagreement Std: {triadCurrentState.disagreement}
              </span>
            </div>
            <div className="text-lg font-bold text-white mt-1">
              ACTION: CASH PRESERVATION (ORDER REJECTED)
            </div>
            <p className="text-xs text-zinc-400 mt-0.5">
              Route Gamma has vetoed Alpha (+65) and Beta (+80). Capital remains 100% sheltered in settled funds.
            </p>
          </div>
        </div>

        <div className="text-right shrink-0 font-mono text-xs text-zinc-400 bg-zinc-950/80 p-3 rounded-lg border border-zinc-800">
          <div>Consensus Score: <strong className="text-rose-400">-85.00</strong></div>
          <div>Taleb Veto Status: <strong className="text-rose-400">ACTIVE</strong></div>
          <div>Inter-Agent Conflict: <strong className="text-amber-400">SEVERE</strong></div>
        </div>
      </div>

      {/* 3. Bottom Section: The AI Trade Audit Journal (RAG Synthesis Memo) */}
      <div className="bg-zinc-900/90 border border-zinc-800 rounded-xl p-6 shadow-xl space-y-4">
        <div className="flex justify-between items-center border-b border-zinc-800 pb-3">
          <div className="flex items-center space-x-2 text-sm font-bold text-white tracking-wide">
            <FileText className="w-4 h-4 text-indigo-400" />
            <span>AI AUDIT MEMO (LOCAL LLAMA-3 & PGVECTOR RAG PIPELINE)</span>
          </div>
          <span className="text-[10px] font-mono bg-zinc-800 text-zinc-400 px-2 py-0.5 rounded border border-zinc-700">
            1536-DIM EMBEDDINGS
          </span>
        </div>

        <div className="bg-zinc-950 border border-zinc-800/80 rounded-lg p-5 font-mono text-xs text-zinc-300 leading-relaxed whitespace-pre-wrap">
          {journalMemoMarkdown}
        </div>
      </div>
    </div>
  );
}
