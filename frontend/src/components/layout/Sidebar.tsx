"use client";

import React from "react";
import { FolderKanban, Network, Brain } from "lucide-react";

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export default function Sidebar({ activeTab, setActiveTab }: SidebarProps) {
  const menuItems = [
    { id: "explorer", name: "Memory Explorer", icon: FolderKanban },
    { id: "graph", name: "Knowledge Graph", icon: Network },
    { id: "chat", name: "RAG Assistant", icon: Brain },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col min-h-screen text-slate-300">
      {/* Brand Logo */}
      <div className="h-16 flex items-center gap-3 px-6 border-b border-slate-800">
        <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-cyan-400 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
          <span className="text-white font-black text-sm">E</span>
        </div>
        <span className="text-lg font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
          EchoMesh AI
        </span>
      </div>

      {/* Navigation Items */}
      <nav className="flex-1 px-4 py-6 space-y-1.5">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 text-left ${
                isActive
                  ? "bg-gradient-to-r from-cyan-500/10 to-blue-500/5 text-cyan-400 border-l-2 border-cyan-400 pl-[14px]"
                  : "hover:bg-slate-800/60 hover:text-slate-100"
              }`}
            >
              <Icon className={`h-5 w-5 ${isActive ? "text-cyan-400" : "text-slate-400"}`} />
              {item.name}
            </button>
          );
        })}
      </nav>

      {/* Footer Info */}
      <div className="p-4 border-t border-slate-800 text-xs text-slate-500 space-y-1">
        <div>EchoMesh AI OS</div>
        <div className="flex items-center gap-1">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
          CockroachDB Connected
        </div>
      </div>
    </aside>
  );
}
