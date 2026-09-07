"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Brain,
  Layers,
  FlaskConical,
  ListFilter,
  RotateCcw,
  ExternalLink,
  Terminal,
} from "lucide-react";

interface NavItem {
  name: string;
  href: string;
  icon: React.ElementType;
  badge?: string;
  badgeColor?: string;
}

const navItems: NavItem[] = [
  {
    name: "Executive Overview",
    href: "/",
    icon: LayoutDashboard,
  },
  {
    name: "AI Consciousness",
    href: "/consciousness",
    icon: Brain,
    badge: "TRIAD",
    badgeColor: "bg-indigo-950 text-indigo-400 border-indigo-800",
  },
  {
    name: "Daily Decision Matrix",
    href: "/decisions",
    icon: ListFilter,
    badge: "NON-ACTION",
    badgeColor: "bg-zinc-800 text-zinc-300 border-zinc-700",
  },
  {
    name: "Epistemic Reflections",
    href: "/reflections",
    icon: RotateCcw,
    badge: "CRITIC",
    badgeColor: "bg-rose-950 text-rose-400 border-rose-800",
  },
  {
    name: "Portfolio & Ledger",
    href: "/portfolio",
    icon: Layers,
    badge: "T+2",
    badgeColor: "bg-emerald-950 text-emerald-400 border-emerald-800",
  },
  {
    name: "Research & Stress Lab",
    href: "/research",
    icon: FlaskConical,
    badge: "FALSIFIED",
    badgeColor: "bg-purple-950 text-purple-400 border-purple-800",
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-zinc-800/80 bg-zinc-950 flex flex-col justify-between shrink-0 select-none">
      <div className="p-4 space-y-6">
        {/* Brand Header */}
        <div className="flex items-center space-x-3 px-2 py-1">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 via-purple-600 to-rose-500 flex items-center justify-center text-white shadow-lg shadow-indigo-950/50">
            <Terminal className="w-4 h-4" />
          </div>
          <div>
            <div className="font-bold text-sm tracking-tight text-white flex items-center gap-1.5">
              <span>COGNITIVE TRIAD</span>
            </div>
            <div className="text-[10px] font-mono tracking-widest text-zinc-400 uppercase">
              NEPSE Terminal v1.0
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                  isActive
                    ? "bg-zinc-900 text-white border border-zinc-800 shadow-sm"
                    : "text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/50"
                }`}
              >
                <div className="flex items-center space-x-3">
                  <Icon
                    className={`w-4 h-4 ${
                      isActive ? "text-indigo-400" : "text-zinc-400"
                    }`}
                  />
                  <span>{item.name}</span>
                </div>
                {item.badge && (
                  <span
                    className={`text-[9px] font-mono font-bold px-1.5 py-0.5 rounded border ${
                      item.badgeColor || "bg-zinc-800 text-zinc-400 border-zinc-700"
                    }`}
                  >
                    {item.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Terminal System Status Footer */}
      <div className="p-4 border-t border-zinc-800/80 space-y-3">
        <div className="bg-zinc-900/80 border border-zinc-800 p-3 rounded-lg space-y-2">
          <div className="flex items-center justify-between text-[11px]">
            <span className="text-zinc-400 font-medium">System Core</span>
            <span className="flex items-center space-x-1.5 text-emerald-400 font-mono text-[10px]">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>NOMINAL</span>
            </span>
          </div>
          <div className="flex items-center justify-between text-[11px]">
            <span className="text-zinc-400 font-medium">Settlement Cycle</span>
            <span className="text-zinc-200 font-mono text-[10px]">T+2 Working Days</span>
          </div>
          <div className="flex items-center justify-between text-[11px]">
            <span className="text-zinc-400 font-medium">Taleb Veto Guard</span>
            <span className="text-amber-400 font-mono text-[10px]">ARMED</span>
          </div>
        </div>

        <a
          href="http://localhost:8000/docs"
          target="_blank"
          rel="noopener noreferrer"
          className="w-full py-2 px-3 bg-zinc-900 hover:bg-zinc-800 text-zinc-300 rounded-lg text-[11px] font-mono flex items-center justify-center space-x-2 border border-zinc-800 transition"
        >
          <ExternalLink className="w-3 h-3 text-zinc-400" />
          <span>OpenAPI Docs (:8000)</span>
        </a>
      </div>
    </aside>
  );
}
