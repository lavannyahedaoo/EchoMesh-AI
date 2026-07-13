"use client";

import React from "react";
import { useWorkspace } from "../../context/WorkspaceContext";
import { Users, Layers } from "lucide-react";

interface TeamItem {
  id: string;
  name: string;
}

interface ProjectItem {
  id: string;
  name: string;
}

interface HeaderProps {
  teams?: TeamItem[];
  projects?: ProjectItem[];
  isLoadingTeams?: boolean;
  isLoadingProjects?: boolean;
}

export default function Header({
  teams = [],
  projects = [],
  isLoadingTeams = false,
  isLoadingProjects = false,
}: HeaderProps) {
  const { activeTeamId, setActiveTeamId, activeProjectId, setActiveProjectId } = useWorkspace();

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/60 backdrop-blur-xl flex items-center justify-between px-8 text-slate-300">
      <div className="flex items-center gap-6">
        <h2 className="text-sm font-semibold tracking-wider text-slate-400 uppercase">
          System Panel
        </h2>
      </div>

      <div className="flex items-center gap-4">
        {/* Workspace Team Switcher */}
        <div className="flex items-center gap-2 bg-slate-950/60 border border-slate-800/80 px-3 py-1.5 rounded-xl">
          <Users className="h-4 w-4 text-cyan-400" />
          <select
            value={activeTeamId || ""}
            onChange={(e) => {
              const val = e.target.value;
              setActiveTeamId(val || null);
              setActiveProjectId(null); // Reset project on team switch
            }}
            className="bg-transparent text-sm font-medium text-slate-200 outline-none border-none cursor-pointer max-w-[160px] focus:ring-0"
            disabled={isLoadingTeams}
          >
            <option value="" className="bg-slate-900 text-slate-400">Select Team...</option>
            {teams.map((t) => (
              <option key={t.id} value={t.id} className="bg-slate-900 text-slate-200">
                {t.name}
              </option>
            ))}
          </select>
        </div>

        {/* Project Switcher */}
        <div className="flex items-center gap-2 bg-slate-950/60 border border-slate-800/80 px-3 py-1.5 rounded-xl">
          <Layers className="h-4 w-4 text-blue-400" />
          <select
            value={activeProjectId || ""}
            onChange={(e) => setActiveProjectId(e.target.value || null)}
            className="bg-transparent text-sm font-medium text-slate-200 outline-none border-none cursor-pointer max-w-[160px] focus:ring-0"
            disabled={isLoadingProjects || !activeTeamId}
          >
            <option value="" className="bg-slate-900 text-slate-400">All Projects</option>
            {projects.map((p) => (
              <option key={p.id} value={p.id} className="bg-slate-900 text-slate-200">
                {p.name}
              </option>
            ))}
          </select>
        </div>
      </div>
    </header>
  );
}
