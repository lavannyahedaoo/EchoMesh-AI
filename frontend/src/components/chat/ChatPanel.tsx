"use client";

import React, { useState, useRef, useEffect } from "react";
import { useSearch } from "../../hooks/useApi";
import { useWorkspace } from "../../context/WorkspaceContext";
import { Memory } from "../../types";
import { Send, Trash2, Bot, User, CornerDownRight, Loader2 } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Memory[];
  timestamp: Date;
}

export default function ChatPanel() {
  const { activeTeamId } = useWorkspace();
  const searchMutation = useSearch();

  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !activeTeamId) return;

    const userQuery = input.trim();
    setInput("");

    const userMsgId = Math.random().toString(36).substring(7);
    const userMessage: Message = {
      id: userMsgId,
      role: "user",
      content: userQuery,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);

    const assistantMsgId = Math.random().toString(36).substring(7);

    try {
      const matchingMemories = await searchMutation.mutateAsync({
        query: userQuery,
        team_id: activeTeamId,
        limit: 3,
        threshold: 0.2,
      });

      let synthesizedResponse = "";
      if (matchingMemories.length === 0) {
        synthesizedResponse = "I searched the knowledge base but found no related documents or decisions for this query in the current workspace. Try adjusting your search query.";
      } else {
        const memoryTitles = matchingMemories.map((m) => `"${m.title}"`).join(", ");
        synthesizedResponse = `Based on the matching workspace memories (${memoryTitles}), here is the synthesized summary:\n\n`;
        
        matchingMemories.forEach((m, idx) => {
          synthesizedResponse += `${idx + 1}. **${m.title}** (Type: ${m.memory_type}): ${m.summary}\n`;
        });
        
        synthesizedResponse += `\n*Note: This response is compiled directly from the retrieved semantic database context.*`;
      }

      const assistantMessage: Message = {
        id: assistantMsgId,
        role: "assistant",
        content: synthesizedResponse,
        sources: matchingMemories,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      const assistantMessage: Message = {
        id: assistantMsgId,
        role: "assistant",
        content: `Error executing search pipeline query: ${err.message || "Unknown API failure."}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)] border border-slate-800 rounded-3xl bg-slate-900/20 backdrop-blur-xl overflow-hidden">
      {/* Panel Header */}
      <div className="px-6 py-4 border-b border-slate-800 bg-slate-900/60 backdrop-blur-md flex justify-between items-center text-slate-300">
        <div className="flex items-center gap-2">
          <Bot className="h-5 w-5 text-cyan-400" />
          <div>
            <h3 className="font-bold text-slate-200 text-sm">EchoMesh Cognitive RAG Assistant</h3>
            <p className="text-[10px] text-slate-500">Queries matching vector memories context</p>
          </div>
        </div>
        {messages.length > 0 && (
          <button
            onClick={handleClearChat}
            className="flex items-center gap-1 text-xs text-rose-400 hover:text-rose-300 transition-colors font-medium border border-rose-500/20 px-2.5 py-1 rounded-lg bg-rose-500/5 hover:bg-rose-500/10"
          >
            <Trash2 className="h-3.5 w-3.5" />
            Clear
          </button>
        )}
      </div>

      {/* Message History Grid */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center text-slate-500 max-w-md mx-auto">
            <span className="text-4xl mb-4">💬</span>
            <h4 className="text-slate-300 font-semibold text-sm">Ask EchoMesh AI</h4>
            <p className="text-xs text-slate-500 leading-relaxed mt-1.5">
              Enter queries about architectural choices, engineering meeting results, and project logs.
              The assistant will query your vector index and display matching database context.
            </p>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-4 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              {msg.role === "assistant" && (
                <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-cyan-400 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 shrink-0">
                  <Bot className="h-4 w-4 text-white" />
                </div>
              )}

              <div className={`max-w-[75%] rounded-2xl p-4 text-sm leading-relaxed border ${
                msg.role === "user"
                  ? "bg-slate-800 border-slate-700 text-slate-100 rounded-tr-none"
                  : "bg-slate-900 border-slate-800 text-slate-300 rounded-tl-none space-y-3"
              }`}>
                <div className="whitespace-pre-wrap">{msg.content}</div>

                {msg.sources && msg.sources.length > 0 && (
                  <div className="border-t border-slate-800/80 pt-3 mt-3">
                    <h5 className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                      <CornerDownRight className="h-3 w-3 text-cyan-400" /> Matches
                    </h5>
                    <div className="grid grid-cols-1 gap-2">
                      {msg.sources.map((src) => (
                        <div
                          key={src.id}
                          className="flex items-center justify-between p-2 rounded-lg bg-slate-950/40 border border-slate-850 text-xs text-slate-400"
                        >
                          <span className="font-medium truncate pr-4">{src.title}</span>
                          <span className="text-[10px] uppercase text-cyan-400 border border-cyan-500/20 bg-cyan-500/5 px-1.5 py-0.5 rounded shrink-0">
                            {src.memory_type}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {msg.role === "user" && (
                <div className="h-8 w-8 rounded-lg bg-slate-800 flex items-center justify-center shrink-0 border border-slate-700">
                  <User className="h-4 w-4 text-slate-300" />
                </div>
              )}
            </div>
          ))
        )}

        {searchMutation.isPending && (
          <div className="flex gap-4 justify-start">
            <div className="h-8 w-8 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center shrink-0">
              <Bot className="h-4 w-4 text-cyan-400" />
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-none p-4 text-xs text-slate-500 flex items-center gap-2">
              <Loader2 className="h-3.5 w-3.5 animate-spin text-cyan-400" />
              <span>Querying vector similarity indexes...</span>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <form
        onSubmit={handleSubmit}
        className="p-4 bg-slate-900/40 border-t border-slate-800/85 flex gap-3"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={activeTeamId ? "Ask a question about the workspace..." : "Select team workspace in the header first"}
          disabled={!activeTeamId || searchMutation.isPending}
          className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-650 focus:outline-none focus:border-cyan-500 transition-colors disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!activeTeamId || !input.trim() || searchMutation.isPending}
          className="px-5 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-sm font-semibold text-white shadow-lg shadow-cyan-500/20 active:scale-95 transition-all flex items-center justify-center disabled:opacity-50 disabled:pointer-events-none"
        >
          <Send className="h-4 w-4" />
        </button>
      </form>
    </div>
  );
}
