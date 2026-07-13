"use client";

import React, { useState } from "react";
import { useIngest } from "../../hooks/useApi";
import { useWorkspace } from "../../context/WorkspaceContext";
import { X, Loader } from "lucide-react";

interface IngestModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function IngestModal({ isOpen, onClose }: IngestModalProps) {
  const { activeTeamId, activeProjectId } = useWorkspace();
  const ingestMutation = useIngest();

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [memoryType, setMemoryType] = useState("document");
  const [importance, setImportance] = useState(3);
  const [confidence, setConfidence] = useState(1.0);
  const [chunkSize, setChunkSize] = useState(1000);
  const [chunkOverlap, setChunkOverlap] = useState(200);
  const [errorMessage, setErrorMessage] = useState("");

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");

    if (!activeTeamId) {
      setErrorMessage("Please select a team workspace context in the header first.");
      return;
    }

    if (!title.trim() || !content.trim()) {
      setErrorMessage("Title and content are required.");
      return;
    }

    try {
      await ingestMutation.mutateAsync({
        title,
        content,
        memory_type: memoryType,
        team_id: activeTeamId,
        project_id: activeProjectId,
        importance,
        confidence_score: confidence,
        meta_data: { environment: "development", source: "client_portal" },
        chunk_size: chunkSize,
        chunk_overlap: chunkOverlap,
      });
      setTitle("");
      setContent("");
      setMemoryType("document");
      setImportance(3);
      setConfidence(1.0);
      onClose();
    } catch (err: any) {
      setErrorMessage(err.message || "Ingestion failed.");
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <h3 className="font-bold text-slate-200 text-lg">Ingest New Memory</h3>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300">
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4 overflow-y-auto flex-1 text-slate-300">
          {errorMessage && (
            <div className="p-3 bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs rounded-xl">
              {errorMessage}
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1.5">
              Title
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. CockroachDB Cloud Migration Choice"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-600 focus:outline-none focus:border-cyan-500 transition-colors"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1.5">
              Content Payload
            </label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Enter details, transcripts, decision records, or markdown text..."
              rows={5}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-600 focus:outline-none focus:border-cyan-500 transition-colors resize-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase mb-1.5">
                Type
              </label>
              <select
                value={memoryType}
                onChange={(e) => setMemoryType(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-sm text-slate-300 focus:outline-none focus:border-cyan-500 transition-colors"
              >
                <option value="document">Document</option>
                <option value="decision">Decision</option>
                <option value="meeting">Meeting</option>
                <option value="task">Task</option>
                <option value="note">Note</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase mb-1.5">
                Importance (1-5)
              </label>
              <select
                value={importance}
                onChange={(e) => setImportance(Number(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-sm text-slate-300 focus:outline-none focus:border-cyan-500 transition-colors"
              >
                <option value="1">1 (Low)</option>
                <option value="2">2</option>
                <option value="3">3 (Normal)</option>
                <option value="4">4</option>
                <option value="5">5 (Critical)</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase mb-1.5">
                Chunk Size
              </label>
              <input
                type="number"
                value={chunkSize}
                onChange={(e) => setChunkSize(Number(e.target.value))}
                min={100}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 transition-colors"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 uppercase mb-1.5">
                Overlap
              </label>
              <input
                type="number"
                value={chunkOverlap}
                onChange={(e) => setChunkOverlap(Number(e.target.value))}
                min={0}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 transition-colors"
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="pt-4 flex justify-end gap-3 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="px-5 py-2.5 rounded-xl border border-slate-800 hover:border-slate-700 text-sm font-medium text-slate-300 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={ingestMutation.isPending}
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-sm font-medium text-white shadow-lg shadow-cyan-500/20 transition-all flex items-center gap-2"
            >
              {ingestMutation.isPending ? (
                <>
                  <Loader className="h-4 w-4 animate-spin" />
                  Ingesting...
                </>
              ) : (
                "Ingest Memory"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
