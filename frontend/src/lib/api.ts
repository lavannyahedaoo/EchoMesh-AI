import { Team, Project, Memory, MemoryIngestRequest, MemorySearchRequest } from "../types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorDetail = "";
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.detail || response.statusText;
    } catch {
      errorDetail = response.statusText;
    }
    throw new Error(errorDetail || `API request failed with status ${response.status}`);
  }
  return response.json();
}

export const api = {
  async getTeams(): Promise<Team[]> {
    const res = await fetch(`${API_BASE_URL}/teams/`);
    return handleResponse<Team[]>(res);
  },

  async getProjects(): Promise<Project[]> {
    const res = await fetch(`${API_BASE_URL}/projects/`);
    return handleResponse<Project[]>(res);
  },

  async getMemories(skip: number = 0, limit: number = 100): Promise<Memory[]> {
    const res = await fetch(`${API_BASE_URL}/memories/?skip=${skip}&limit=${limit}`);
    return handleResponse<Memory[]>(res);
  },

  async ingestMemory(payload: MemoryIngestRequest): Promise<Memory[]> {
    const res = await fetch(`${API_BASE_URL}/memories/ingest`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    return handleResponse<Memory[]>(res);
  },

  async searchMemories(payload: MemorySearchRequest): Promise<Memory[]> {
    const res = await fetch(`${API_BASE_URL}/memories/search`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    return handleResponse<Memory[]>(res);
  },
};
