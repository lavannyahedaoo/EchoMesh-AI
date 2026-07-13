"use client";

import React, { useState } from "react";
import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import MemoryGrid from "../components/explorer/MemoryGrid";
import GraphCanvas from "../components/graph/GraphCanvas";
import { useTeams, useProjects } from "../hooks/useApi";
import { useWorkspace } from "../context/WorkspaceContext";

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<string>("explorer");
  const { activeTeamId } = useWorkspace();

  // Query workspaces teams and projects
  const { data: teams = [], isLoading: isLoadingTeams } = useTeams();
  const { data: projects = [], isLoading: isLoadingProjects } = useProjects();

  // Filter projects by active team boundary
  const filteredProjects = projects.filter((p) => p.team_id === activeTeamId);

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-950 text-slate-100 font-sans">
      {/* Sidebar Navigation */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Header Switchers */}
        <Header 
          teams={teams} 
          projects={filteredProjects} 
          isLoadingTeams={isLoadingTeams}
          isLoadingProjects={isLoadingProjects}
        />

        {/* Tab View Panels */}
        <main className="flex-1 overflow-auto p-8 relative">
          {activeTab === "explorer" && (
            <div className="space-y-6">
              <div>
                <h1 className="text-3xl font-bold tracking-tight">Memory Explorer</h1>
                <p className="text-slate-400 text-sm mt-1">Explore and filter architectural memories.</p>
              </div>
              <MemoryGrid />
            </div>
          )}

          {activeTab === "graph" && (
            <div className="space-y-6 h-full flex flex-col">
              <div>
                <h1 className="text-3xl font-bold tracking-tight">Knowledge Graph</h1>
                <p className="text-slate-400 text-sm mt-1">Visualize topological relations between decisions and links.</p>
              </div>
              <GraphCanvas />
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
