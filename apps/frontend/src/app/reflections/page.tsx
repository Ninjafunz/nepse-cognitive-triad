"use client";

import React, { useState } from "react";
import {
  Brain,
  AlertTriangle,
  RotateCcw,
  CheckCircle2,
  XCircle,
  FileText,
  HelpCircle,
  BookOpen,
} from "lucide-react";
import { predictionReflectionsData } from "@/lib/evaluationsData";

export default function ReflectionsPage() {
  const [selectedReflection, setSelectedReflection] = useState(
    predictionReflectionsData[0]
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-zinc-900/90 border border-zinc-800 p-5 rounded-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-lg bg-rose-950 border border-rose-800 flex items-center justify-center text-rose-400 shadow-md">
            <RotateCcw className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white tracking-tight">
              EPISTEMIC REFLECTION ENGINE: THE GRAVEYARD OF ERRORS
            </h1>
            <p className="text-xs text-zinc-400 font-mono">
              Self-correcting critic loop • Post-mortem decomposition of failed predictions & behavioral blindspots
            </p>
          </div>
        </div>

        <div className="bg-zinc-950 px-3 py-1.5 rounded-lg border border-zinc-800 text-xs font-mono text-zinc-400">
          Target Window: <strong className="text-zinc-200">T+5 Trading Days</strong> | Paradigm: <strong className="text-indigo-400">Popperian Falsification</strong>
        </div>
      </div>

      {/* Main Split Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: List of Predictions (40%) */}
        <div className="lg:col-span-5 space-y-3">
          <div className="text-xs font-mono text-zinc-400 uppercase tracking-wider px-1">
            Historical Predictions (T+5 Audit)
          </div>

          <div className="space-y-3">
            {predictionReflectionsData.map((item) => {
              const isSelected = selectedReflection.id === item.id;
              const isFail = !item.wasCorrect;

              return (
                <div
                  key={item.id}
                  onClick={() => setSelectedReflection(item)}
                  className={`p-4 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? "bg-zinc-900 border-zinc-600 shadow-lg"
                      : "bg-zinc-950/80 border-zinc-800/80 hover:border-zinc-700"
                  }`}
                >
                  <div className="flex items-center justify-between text-xs font-mono">
                    <div className="flex items-center space-x-2">
                      <span className="font-bold text-white text-sm">{item.symbol}</span>
                      <span className="text-zinc-500">
                        {item.predictionDate} → {item.targetDate}
                      </span>
                    </div>
                    {isFail ? (
                      <span className="flex items-center space-x-1 text-rose-400 font-bold bg-rose-950/80 px-2 py-0.5 rounded border border-rose-900 text-[10px]">
                        <XCircle className="w-3 h-3" />
                        <span>FAILED ({item.actualReturnPct}%)</span>
                      </span>
                    ) : (
                      <span className="flex items-center space-x-1 text-emerald-400 font-bold bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-900 text-[10px]">
                        <CheckCircle2 className="w-3 h-3" />
                        <span>CORROBORATED (+{item.actualReturnPct}%)</span>
                      </span>
                    )}
                  </div>

                  <p className="text-xs text-zinc-300 font-sans mt-2 line-clamp-2 leading-relaxed">
                    {item.predictedThesis}
                  </p>

                  <div className="flex items-center justify-between pt-2 mt-2 border-t border-zinc-800 text-[11px] font-mono">
                    <span className="text-zinc-500">
                      Failing Component: <strong className="text-zinc-300">Route {item.failedRoute}</strong>
                    </span>
                    <span className="text-indigo-400 hover:underline">
                      View Post-Mortem →
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Selected Post-Mortem Audit Report (60%) */}
        <div className="lg:col-span-7 bg-zinc-900/90 border border-zinc-800 rounded-xl p-6 shadow-xl space-y-4">
          <div className="flex justify-between items-start border-b border-zinc-800 pb-3">
            <div>
              <div className="flex items-center space-x-2">
                <span
                  className={`text-xs font-mono font-bold px-2 py-0.5 rounded border ${
                    !selectedReflection.wasCorrect
                      ? "bg-rose-950 text-rose-300 border-rose-800"
                      : "bg-emerald-950 text-emerald-300 border-emerald-800"
                  }`}
                >
                  {!selectedReflection.wasCorrect
                    ? "EPISTEMIC FAILURE AUDIT"
                    : "EMPIRICAL CORROBORATION"}
                </span>
                <span className="text-xs font-mono text-zinc-400">
                  Symbol: <strong className="text-white">{selectedReflection.symbol}</strong>
                </span>
              </div>
              <h2 className="text-sm font-bold text-white mt-1.5">
                {selectedReflection.epistemicConcept}
              </h2>
            </div>
            <div className="text-right text-[11px] font-mono text-zinc-500">
              Reflected: {selectedReflection.reflectedAt}
            </div>
          </div>

          {/* Quick Metrics Bar */}
          <div className="grid grid-cols-3 gap-3 bg-zinc-950 p-3 rounded-lg border border-zinc-800 text-xs font-mono">
            <div>
              <span className="text-zinc-500 block text-[10px]">PREDICTION THESIS</span>
              <span className="text-zinc-200">{selectedReflection.expectedDirection} TARGET</span>
            </div>
            <div>
              <span className="text-zinc-500 block text-[10px]">ACTUAL OUTCOME</span>
              <span
                className={`font-bold ${
                  selectedReflection.actualReturnPct < 0
                    ? "text-rose-400"
                    : "text-emerald-400"
                }`}
              >
                {selectedReflection.actualReturnPct > 0 ? "+" : ""}
                {selectedReflection.actualReturnPct}% in 5 Days
              </span>
            </div>
            <div>
              <span className="text-zinc-500 block text-[10px]">PRIMARY ROOT CAUSE</span>
              <span className="text-amber-400 font-bold">Route {selectedReflection.failedRoute}</span>
            </div>
          </div>

          {/* Full Markdown Self-Correction Report */}
          <div className="bg-zinc-950 p-5 rounded-lg border border-zinc-800 font-mono text-xs text-zinc-300 whitespace-pre-wrap leading-relaxed">
            {selectedReflection.reflectionJournal}
          </div>

          {/* Corrective Action Takeaway */}
          <div className="p-4 rounded-lg bg-indigo-950/30 border border-indigo-900/60 space-y-1">
            <div className="text-xs font-bold font-mono text-indigo-400 uppercase tracking-wider">
              Enforced Systemic Heuristic
            </div>
            <p className="text-xs text-zinc-300 font-sans leading-relaxed">
              {selectedReflection.correctiveAction}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
