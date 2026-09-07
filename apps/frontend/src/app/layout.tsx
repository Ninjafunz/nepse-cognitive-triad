import type { Metadata } from "next";
import Sidebar from "@/components/layout/Sidebar";
import Header from "@/components/layout/Header";
import "./globals.css";

export const metadata: Metadata = {
  title: "NEPSE Cognitive Triad — Hedge Fund Terminal",
  description: "Literature-Grounded Multi-Agent Algorithmic Trading Platform for the Nepal Stock Exchange",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-zinc-950 text-zinc-100 min-h-screen antialiased flex overflow-hidden font-sans">
        {/* Left Navigation Sidebar */}
        <Sidebar />

        {/* Right Application Body */}
        <div className="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
          <Header />
          <main className="flex-1 overflow-y-auto p-6 bg-zinc-950/60">
            <div className="max-w-7xl mx-auto">{children}</div>
          </main>
        </div>
      </body>
    </html>
  );
}
