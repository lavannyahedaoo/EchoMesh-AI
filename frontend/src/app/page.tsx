"use client";

import React, { useState } from "react";
import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<string>("explorer");

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-950 text-slate-100 font-sans">
      {/* Sidebar Navigation */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Header Switchers */}
        <Header />

        {/* Tab View Panels */}
        <main className="flex-1 overflow-auto p-8 relative">
          {activeTab === "explorer" && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <div>
                  <h1 className="text-3xl font-bold tracking-tight">Memory Explorer</h1>
                  <p className="text-slate-400 text-sm mt-1">Explore and filter architectural memories.</p>
                </div>
              </div>
              <div className="p-8 border border-dashed border-slate-800 rounded-2xl flex flex-col items-center justify-center text-center text-slate-500 min-h-[300px]">
                <span className="text-3xl mb-2">📥</span>
                <p className="text-sm font-medium text-slate-400">Memory grid content placeholder</p>
                <p className="text-xs text-slate-600 mt-1">API integration will load real records here in the next step.</p>
              </div>
            </div>
          )}

          {activeTab === "graph" && (
            <div className="space-y-6 h-full flex flex-col">
              <div>
                <h1 className="text-3xl font-bold tracking-tight">Knowledge Graph</h1>
                <p className="text-slate-400 text-sm mt-1">Visualize topological relations between decisions and links.</p>
              </div>
              <div className="flex-1 p-8 border border-dashed border-slate-800 rounded-2xl flex flex-col items-center justify-center text-center text-slate-500 min-h-[300px]">
                <span className="text-3xl mb-2">🔗</span>
                <p className="text-sm font-medium text-slate-400">Interactive graph visualization canvas placeholder</p>
                <p className="text-xs text-slate-600 mt-1">Graph Canvas will display network linkages in Step 4.</p>
              </div>
            </div>
          )}

          {activeTab === "chat" && (
            <div className="space-y-6 h-full flex flex-col">
              <div>
                <h1 className="text-3xl font-bold tracking-tight">RAG Assistant</h1>
                <p className="text-slate-400 text-sm mt-1">Ask questions about architectural logic and choices.</p>
              </div>
              <div className="flex-1 p-8 border border-dashed border-slate-800 rounded-2xl flex flex-col items-center justify-center text-center text-slate-500 min-h-[300px]">
                <span className="text-3xl mb-2">🧠</span>
                <p className="text-sm font-medium text-slate-400">LLM Chatbot workspace panel placeholder</p>
                <p className="text-xs text-slate-600 mt-1">AI Chatbot queries will be wired in Step 5.</p>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
