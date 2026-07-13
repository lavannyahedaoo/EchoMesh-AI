"use client";

import React, { useState, useEffect } from "react";
import { useMemories, useSearch } from "../../hooks/useApi";
import { useWorkspace } from "../../context/WorkspaceContext";
import { Search, Plus, Calendar, AlertCircle, X, ChevronRight } from "lucide-react";
import IngestModal from "./IngestModal";
import { Memory } from "../../types";

export default function MemoryGrid() {
  const { activeTeamId, activeProjectId } = useWorkspace();
  const { data: defaultMemories = [], isLoading: isLoadingMemories, error: errorMemories } = useMemories();
  const searchMutation = useSearch();

  const [searchQuery, setSearchQuery] = useState("");
  const [activeResults, setActiveResults] = useState<Memory[] | null>(null);
  const [selectedMemory, setSelectedMemory] = useState<Memory | null>(null);
  const [isIngestOpen, setIsIngestOpen] = useState(false);

  useEffect(() => {
    setActiveResults(null);
    setSearchQuery("");
  }, [activeTeamId, activeProjectId]);

  const handleSearchSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeTeamId) return;

    if (!searchQuery.trim()) {
      setActiveResults(null);
      return;
    }

    try {
      const results = await searchMutation.mutateAsync({
        query: searchQuery,
        team_id: activeTeamId,
        limit: 10,
        threshold: 0.5,
      });
      setActiveResults(results);
    } catch (err) {
      console.error("Vector search failed", err);
    }
  };

  const handleClearSearch = () => {
    setSearchQuery("");
    setActiveResults(null);
  };

  const displayedMemories = activeResults !== null 
    ? activeResults 
    : defaultMemories.filter((m) => {
        const teamMatch = m.team_id === activeTeamId;
        const projectMatch = !activeProjectId || m.project_id === activeProjectId;
        return teamMatch && projectMatch;
      });

  const getImportanceColor = (imp: number) => {
    if (imp >= 5) return "bg-rose-500/10 text-rose-400 border border-rose-500/20";
    if (imp >= 4) return "bg-amber-500/10 text-amber-400 border border-amber-500/20";
    return "bg-slate-800 text-slate-400 border border-slate-700";
  };

  const getTypeBadgeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case "decision": return "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20";
      case "meeting": return "bg-purple-500/10 text-purple-400 border border-purple-500/20";
      case "task": return "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20";
      default: return "bg-slate-800 text-slate-300 border border-slate-700";
    }
  };

  return (
    <div className="space-y-6 text-slate-300">
      {/* Search Bar and Ingest Button Container */}
      <div className="flex flex-col sm:flex-row gap-4 justify-between items-stretch sm:items-center bg-slate-900/40 p-4 border border-slate-800/80 rounded-2xl animate-fade-in">
        <form onSubmit={handleSearchSubmit} className="flex-1 flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search memories semantically..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-sm text-slate-100 placeholder-slate-600 focus:outline-none focus:border-cyan-500 transition-colors"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={handleClearSearch}
                className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
          <button
            type="submit"
            disabled={searchMutation.isPending || !activeTeamId}
            className="px-5 py-2 rounded-xl bg-slate-800 hover:bg-slate-750 text-sm font-medium border border-slate-700 hover:border-slate-600 transition-all flex items-center gap-1.5"
          >
            {searchMutation.isPending ? "Searching..." : "Search"}
          </button>
        </form>

        <button
          onClick={() => setIsIngestOpen(true)}
          disabled={!activeTeamId}
          className="px-5 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-sm font-medium text-white shadow-lg shadow-cyan-500/20 transition-all active:scale-95 flex items-center justify-center gap-1.5 disabled:opacity-50 disabled:pointer-events-none"
        >
          <Plus className="h-4 w-4" />
          Ingest Context
        </button>
      </div>

      {/* Main Grid View */}
      {isLoadingMemories ? (
        <div className="p-16 flex flex-col items-center justify-center text-slate-500 animate-fade-in">
          <div className="h-8 w-8 rounded-full border-2 border-cyan-500/30 border-t-cyan-500 animate-spin mb-4" />
          <p className="text-sm">Loading memories context...</p>
        </div>
      ) : errorMemories ? (
        <div className="p-8 border border-red-500/20 bg-red-500/5 rounded-2xl flex items-center gap-3 text-red-400 text-sm animate-fade-in">
          <AlertCircle className="h-5 w-5" />
          <span>Error loading memories: {errorMemories.message}</span>
        </div>
      ) : displayedMemories.length === 0 ? (
        <div className="p-16 border border-dashed border-slate-800 rounded-3xl flex flex-col items-center justify-center text-center text-slate-500 min-h-[300px] animate-fade-in">
          <span className="text-4xl mb-4">📂</span>
          <h3 className="text-slate-300 font-semibold mb-1">No Memories Found</h3>
          <p className="text-sm text-slate-500 max-w-sm">
            {!activeTeamId 
              ? "Select a team workspace context in the header to view memories." 
              : "No memories ingested yet for this context. Click 'Ingest Context' to add some."}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
          {displayedMemories.map((m) => (
            <div
              key={m.id}
              onClick={() => setSelectedMemory(m)}
              className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-xl hover:border-cyan-500/40 hover:-translate-y-0.5 transition-all duration-300 cursor-pointer flex flex-col justify-between group h-full"
            >
              <div>
                <div className="flex justify-between items-start gap-4 mb-4">
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold uppercase ${getTypeBadgeColor(m.memory_type)}`}>
                    {m.memory_type}
                  </span>
                  <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${getImportanceColor(m.importance)}`}>
                    Imp {m.importance}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-200 group-hover:text-cyan-400 transition-colors mb-2 line-clamp-1">
                  {m.title}
                </h3>
                <p className="text-sm text-slate-400 leading-relaxed line-clamp-3 mb-4">
                  {m.summary}
                </p>
              </div>
              <div className="flex items-center justify-between text-xs text-slate-500 border-t border-slate-800/60 pt-4">
                <span className="flex items-center gap-1.5">
                  <Calendar className="h-3.5 w-3.5" />
                  {new Date(m.created_at).toLocaleDateString()}
                </span>
                <span className="flex items-center text-cyan-400 opacity-0 group-hover:opacity-100 transition-opacity font-medium">
                  View Detail
                  <ChevronRight className="h-4 w-4" />
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Memory Detail Modal */}
      {selectedMemory && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl flex flex-col max-h-[85vh] animate-fade-in">
            <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/20">
              <div>
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold uppercase ${getTypeBadgeColor(selectedMemory.memory_type)} mr-2`}>
                  {selectedMemory.memory_type}
                </span>
                <span className="text-xs text-slate-500 font-medium">
                  Created {new Date(selectedMemory.created_at).toLocaleString()}
                </span>
              </div>
              <button onClick={() => setSelectedMemory(null)} className="text-slate-500 hover:text-slate-300">
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-6 flex-1 text-slate-300">
              <div>
                <h2 className="text-2xl font-bold text-slate-100">{selectedMemory.title}</h2>
              </div>

              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Summary</h4>
                <p className="text-sm bg-slate-950/40 p-4 border border-slate-800/50 rounded-xl leading-relaxed text-slate-300">
                  {selectedMemory.summary}
                </p>
              </div>

              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Full Content</h4>
                <div className="text-sm whitespace-pre-wrap leading-relaxed bg-slate-950 p-5 border border-slate-800 rounded-xl text-slate-200 font-light max-h-[250px] overflow-y-auto">
                  {selectedMemory.content}
                </div>
              </div>

              {selectedMemory.meta_data && Object.keys(selectedMemory.meta_data).length > 0 && (
                <div>
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Metadata Context</h4>
                  <pre className="text-xs bg-slate-950/50 p-4 rounded-xl border border-slate-850 overflow-x-auto text-slate-400 font-mono">
                    {JSON.stringify(selectedMemory.meta_data, null, 2)}
                  </pre>
                </div>
              )}
            </div>

            <div className="px-6 py-4 border-t border-slate-800 flex justify-end bg-slate-950/10">
              <button
                onClick={() => setSelectedMemory(null)}
                className="px-5 py-2 rounded-xl bg-slate-800 hover:bg-slate-750 text-sm font-medium text-slate-300 border border-slate-700 transition-colors"
              >
                Close View
              </button>
            </div>
          </div>
        </div>
      )}

      <IngestModal isOpen={isIngestOpen} onClose={() => setIsIngestOpen(false)} />
    </div>
  );
}
