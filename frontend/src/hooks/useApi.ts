import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../lib/api";
import { MemoryIngestRequest, MemorySearchRequest } from "../types";

export function useTeams() {
  return useQuery({
    queryKey: ["teams"],
    queryFn: () => api.getTeams(),
  });
}

export function useProjects() {
  return useQuery({
    queryKey: ["projects"],
    queryFn: () => api.getProjects(),
  });
}

export function useMemories(skip: number = 0, limit: number = 100) {
  return useQuery({
    queryKey: ["memories", skip, limit],
    queryFn: () => api.getMemories(skip, limit),
  });
}

export function useIngest() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: MemoryIngestRequest) => api.ingestMemory(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["memories"] });
    },
  });
}

export function useSearch() {
  return useMutation({
    mutationFn: (payload: MemorySearchRequest) => api.searchMemories(payload),
  });
}
