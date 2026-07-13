"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

interface WorkspaceContextType {
  activeTeamId: string | null;
  setActiveTeamId: (id: string | null) => void;
  activeProjectId: string | null;
  setActiveProjectId: (id: string | null) => void;
}

const WorkspaceContext = createContext<WorkspaceContextType | undefined>(undefined);

export function WorkspaceProvider({ children }: { children: React.ReactNode }) {
  const [activeTeamId, setActiveTeamId] = useState<string | null>(null);
  const [activeProjectId, setActiveProjectId] = useState<string | null>(null);

  useEffect(() => {
    const savedTeam = localStorage.getItem("active_team_id");
    const savedProject = localStorage.getItem("active_project_id");
    if (savedTeam) setActiveTeamId(savedTeam);
    if (savedProject) setActiveProjectId(savedProject);
  }, []);

  const handleSetActiveTeamId = (id: string | null) => {
    setActiveTeamId(id);
    if (id) {
      localStorage.setItem("active_team_id", id);
    } else {
      localStorage.removeItem("active_team_id");
    }
  };

  const handleSetActiveProjectId = (id: string | null) => {
    setActiveProjectId(id);
    if (id) {
      localStorage.setItem("active_project_id", id);
    } else {
      localStorage.removeItem("active_project_id");
    }
  };

  return (
    <WorkspaceContext.Provider
      value={{
        activeTeamId,
        setActiveTeamId: handleSetActiveTeamId,
        activeProjectId,
        setActiveProjectId: handleSetActiveProjectId,
      }}
    >
      {children}
    </WorkspaceContext.Provider>
  );
}

export function useWorkspace() {
  const context = useContext(WorkspaceContext);
  if (!context) {
    throw new Error("useWorkspace must be used within a WorkspaceProvider");
  }
  return context;
}
