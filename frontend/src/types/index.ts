export interface Team {
  id: string;
  name: string;
  created_at: string;
}

export interface Project {
  id: string;
  name: string;
  description: string | null;
  team_id: string;
  created_at: string;
}

export interface Memory {
  id: string;
  title: string;
  summary: string;
  content: string;
  memory_type: string;
  importance: number;
  confidence_score: number;
  embedding_reference: number[] | null;
  created_by: string | null;
  project_id: string | null;
  team_id: string;
  created_at: string;
  updated_at: string;
  meta_data: Record<string, any>;
  status: string;
}

export interface MemoryIngestRequest {
  title: string;
  content: string;
  memory_type: string;
  team_id: string;
  project_id: string | null;
  importance: number;
  confidence_score: number;
  meta_data: Record<string, any> | null;
  chunk_size: number;
  chunk_overlap: number;
}

export interface MemorySearchRequest {
  query: string;
  team_id: string;
  limit: number;
  threshold: number;
}
