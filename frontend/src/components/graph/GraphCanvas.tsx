"use client";

import React, { useState, useEffect, useRef } from "react";
import { useMemories } from "../../hooks/useApi";
import { useWorkspace } from "../../context/WorkspaceContext";
import { Memory } from "../../types";
import { AlertCircle, Calendar, Tag, HardDrive, Info } from "lucide-react";

interface NodePosition {
  x: number;
  y: number;
}

export default function GraphCanvas() {
  const { activeTeamId, activeProjectId } = useWorkspace();
  const { data: memories = [], isLoading, error } = useMemories();

  const filteredMemories = memories.filter(
    (m) => m.team_id === activeTeamId && (!activeProjectId || m.project_id === activeProjectId)
  );

  const [positions, setPositions] = useState<Record<string, NodePosition>>({});
  const [selectedNode, setSelectedNode] = useState<Memory | null>(null);
  const [hoveredNode, setHoveredNode] = useState<Memory | null>(null);
  const [draggedNodeId, setDraggedNodeId] = useState<string | null>(null);
  
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [isPanning, setIsPanning] = useState(false);
  const startPanOffset = useRef({ x: 0, y: 0 });
  const dragStartNodeOffset = useRef({ x: 0, y: 0 });
  
  const canvasRef = useRef<SVGSVGElement | null>(null);

  useEffect(() => {
    if (filteredMemories.length === 0) return;
    
    const newPositions: Record<string, NodePosition> = {};
    const center = { x: 350, y: 250 };
    const radius = Math.min(220, filteredMemories.length * 40 + 60);

    filteredMemories.forEach((m, idx) => {
      if (positions[m.id]) {
        newPositions[m.id] = positions[m.id];
        return;
      }
      const angle = (2 * Math.PI * idx) / filteredMemories.length;
      newPositions[m.id] = {
        x: center.x + radius * Math.cos(angle),
        y: center.y + radius * Math.sin(angle),
      };
    });

    setPositions(newPositions);
  }, [filteredMemories.length, activeTeamId, activeProjectId]);

  const getNodeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case "decision": return "#22d3ee";
      case "meeting": return "#c084fc";
      case "task": return "#34d399";
      default: return "#94a3b8";
    }
  };

  const handleNodeMouseDown = (e: React.MouseEvent, nodeId: string) => {
    e.stopPropagation();
    setDraggedNodeId(nodeId);
    
    const pos = positions[nodeId] || { x: 0, y: 0 };
    dragStartNodeOffset.current = {
      x: e.clientX - pos.x,
      y: e.clientY - pos.y,
    };
  };

  const handleCanvasMouseDown = (e: React.MouseEvent) => {
    if (e.button !== 0) return;
    setIsPanning(true);
    startPanOffset.current = {
      x: e.clientX - pan.x,
      y: e.clientY - pan.y,
    };
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (draggedNodeId) {
      const currentPos = {
        x: e.clientX - dragStartNodeOffset.current.x,
        y: e.clientY - dragStartNodeOffset.current.y,
      };
      setPositions((prev) => ({
        ...prev,
        [draggedNodeId]: currentPos,
      }));
    } else if (isPanning) {
      setPan({
        x: e.clientX - startPanOffset.current.x,
        y: e.clientY - startPanOffset.current.y,
      });
    }
  };

  const handleMouseUp = () => {
    setDraggedNodeId(null);
    setIsPanning(false);
  };

  const handleZoom = (e: React.WheelEvent) => {
    const scaleFactor = 1.1;
    const newZoom = e.deltaY < 0 ? zoom * scaleFactor : zoom / scaleFactor;
    setZoom(Math.max(0.2, Math.min(newZoom, 4)));
  };

  const handleResetView = () => {
    setPan({ x: 0, y: 0 });
    setZoom(1);
  };

  const links: Array<{ source: string; target: string; type: string }> = [];
  for (let i = 0; i < filteredMemories.length; i++) {
    for (let j = i + 1; j < filteredMemories.length; j++) {
      const m1 = filteredMemories[i];
      const m2 = filteredMemories[j];
      
      if (m1.project_id === m2.project_id && m1.project_id !== null) {
        links.push({ source: m1.id, target: m2.id, type: "project" });
      } else if (m1.memory_type === m2.memory_type) {
        links.push({ source: m1.id, target: m2.id, type: "type" });
      }
    }
  }

  return (
    <div className="flex h-[calc(100vh-12rem)] border border-slate-800 rounded-3xl overflow-hidden bg-slate-950/40 backdrop-blur-xl">
      {/* Canvas View Container */}
      <div className="flex-1 relative overflow-hidden select-none">
        {isLoading ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-slate-500">
            <div className="h-8 w-8 rounded-full border-2 border-cyan-500/30 border-t-cyan-500 animate-spin mb-4" />
            <p className="text-sm">Loading graph schema...</p>
          </div>
        ) : error ? (
          <div className="absolute inset-0 flex items-center justify-center p-8 text-red-400 text-sm">
            <AlertCircle className="h-5 w-5 mr-2" />
            Error loading Graph: {error.message}
          </div>
        ) : filteredMemories.length === 0 ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-slate-500 text-center p-6">
            <span className="text-4xl mb-3">🔗</span>
            <p className="text-sm font-semibold text-slate-350">No Graph Nodes</p>
            <p className="text-xs text-slate-650 max-w-xs mt-1">
              {!activeTeamId
                ? "Select a team workspace in the header."
                : "Ingest some memories to see the knowledge graph linkages."}
            </p>
          </div>
        ) : (
          <>
            <div className="absolute top-4 left-4 z-10 flex gap-2">
              <button
                onClick={handleResetView}
                className="px-3.5 py-1.5 rounded-lg bg-slate-900 border border-slate-800 hover:border-slate-700 text-xs font-semibold text-slate-300 transition-colors"
              >
                Reset View
              </button>
            </div>

            {hoveredNode && (
              <div className="absolute bottom-4 left-4 z-10 bg-slate-900/90 border border-slate-800 p-3 rounded-xl max-w-xs shadow-xl text-xs pointer-events-none">
                <div className="font-bold text-slate-200">{hoveredNode.title}</div>
                <div className="text-slate-400 mt-1 line-clamp-2 leading-relaxed">{hoveredNode.summary}</div>
              </div>
            )}

            <svg
              ref={canvasRef}
              className="w-full h-full cursor-grab active:cursor-grabbing"
              onMouseDown={handleCanvasMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
              onMouseLeave={handleMouseUp}
              onWheel={handleZoom}
            >
              <defs>
                <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" strokeWidth="0.5" />
                </pattern>
              </defs>
              <rect width="100%" height="100%" fill="url(#grid)" />

              <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
                {links.map((link, idx) => {
                  const sPos = positions[link.source];
                  const tPos = positions[link.target];
                  if (!sPos || !tPos) return null;
                  return (
                    <line
                      key={idx}
                      x1={sPos.x}
                      y1={sPos.y}
                      x2={tPos.x}
                      y2={tPos.y}
                      stroke={link.type === "project" ? "rgba(56, 189, 248, 0.25)" : "rgba(148, 163, 184, 0.15)"}
                      strokeWidth={link.type === "project" ? "2" : "1.5"}
                      strokeDasharray={link.type === "type" ? "4" : undefined}
                    />
                  );
                })}

                {filteredMemories.map((m) => {
                  const pos = positions[m.id] || { x: 0, y: 0 };
                  const isSelected = selectedNode?.id === m.id;
                  const isHovered = hoveredNode?.id === m.id;
                  const color = getNodeColor(m.memory_type);

                  return (
                    <g
                      key={m.id}
                      transform={`translate(${pos.x}, ${pos.y})`}
                      className="cursor-pointer"
                      onMouseDown={(e) => handleNodeMouseDown(e, m.id)}
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedNode(m);
                      }}
                      onMouseEnter={() => setHoveredNode(m)}
                      onMouseLeave={() => setHoveredNode(null)}
                    >
                      <circle
                        r={22}
                        fill="none"
                        stroke={isSelected ? "#22d3ee" : isHovered ? "rgba(34, 211, 238, 0.4)" : "none"}
                        strokeWidth="2.5"
                      />

                      <circle
                        r={15}
                        fill={color}
                        className="transition-all duration-200"
                        style={{ filter: isSelected || isHovered ? "drop-shadow(0 0 8px " + color + ")" : undefined }}
                      />

                      <circle r={4} fill="#020617" />

                      <text
                        y={32}
                        textAnchor="middle"
                        fill={isSelected ? "#22d3ee" : "#cbd5e1"}
                        className="text-[10px] font-bold select-none"
                      >
                        {m.title.length > 14 ? m.title.substring(0, 12) + "..." : m.title}
                      </text>
                    </g>
                  );
                })}
              </g>
            </svg>
          </>
        )}
      </div>

      {/* Selected Node Details Side Panel */}
      <div className="w-80 border-l border-slate-800 bg-slate-900/20 p-6 flex flex-col justify-between overflow-y-auto">
        {selectedNode ? (
          <div className="space-y-6">
            <div>
              <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase mr-2`} style={{
                backgroundColor: getNodeColor(selectedNode.memory_type) + "15",
                color: getNodeColor(selectedNode.memory_type),
                border: "1px solid " + getNodeColor(selectedNode.memory_type) + "30"
              }}>
                {selectedNode.memory_type}
              </span>
              <h3 className="text-xl font-bold text-slate-100 mt-2">{selectedNode.title}</h3>
            </div>

            <div className="space-y-4">
              <div>
                <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
                  <Info className="h-3 w-3" /> Summary
                </h4>
                <p className="text-sm text-slate-350 mt-1.5 leading-relaxed bg-slate-950/40 border border-slate-800 p-3 rounded-xl">
                  {selectedNode.summary}
                </p>
              </div>

              <div>
                <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
                  <Tag className="h-3 w-3" /> Importance
                </h4>
                <span className="text-xs font-semibold text-slate-300 mt-1 inline-block bg-slate-800 px-2.5 py-0.5 rounded-lg border border-slate-700">
                  Level {selectedNode.importance} / 5
                </span>
              </div>

              <div>
                <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
                  <HardDrive className="h-3 w-3" /> Metadata
                </h4>
                <pre className="text-[10px] bg-slate-950 p-3 rounded-xl border border-slate-850 mt-1.5 overflow-x-auto text-slate-400 font-mono">
                  {JSON.stringify(selectedNode.meta_data, null, 2)}
                </pre>
              </div>

              <div>
                <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
                  <Calendar className="h-3 w-3" /> Timestamps
                </h4>
                <div className="text-xs text-slate-500 space-y-1 mt-1">
                  <div>Created: {new Date(selectedNode.created_at).toLocaleString()}</div>
                  <div>Updated: {new Date(selectedNode.updated_at).toLocaleString()}</div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-slate-650 text-center">
            <span className="text-3xl mb-2">ℹ️</span>
            <p className="text-xs font-medium">Select a node in the graph to view properties.</p>
          </div>
        )}

        {selectedNode && (
          <button
            onClick={() => setSelectedNode(null)}
            className="w-full mt-6 px-4 py-2 bg-slate-800 hover:bg-slate-750 border border-slate-700 text-xs font-semibold rounded-xl text-slate-300 transition-colors"
          >
            Clear Selection
          </button>
        )}
      </div>
    </div>
  );
}
