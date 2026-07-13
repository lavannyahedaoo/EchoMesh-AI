import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class MemoryIngestRequest(BaseModel):
    """
    Request payload schema for ingesting/creating memories.
    """
    title: str = Field(..., description="The main headline or title of the memory.")
    content: str = Field(..., description="The detailed raw text payload to be chunked and stored.")
    memory_type: str = Field("document", description="Classification category (e.g. document, decision, meeting).")
    team_id: uuid.UUID = Field(..., description="UUID of the workspace team tenant.")
    project_id: Optional[uuid.UUID] = Field(None, description="Optional associated project identifier.")
    importance: int = Field(1, ge=1, le=5, description="Importance level from 1 (low) to 5 (critical).")
    confidence_score: float = Field(1.0, ge=0.0, le=1.0, description="Confidence classification rating.")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="Custom JSON metadata attributes.")
    chunk_size: int = Field(1000, gt=0, description="Maximum character length per semantic slice.")
    chunk_overlap: int = Field(200, ge=0, description="Overlapping characters count between sequential slices.")


class MemoryResponse(BaseModel):
    """
    Response schema representing a single retrieved Memory node.
    """
    id: uuid.UUID
    title: str
    summary: str
    content: str
    memory_type: str
    importance: int
    confidence_score: float
    embedding_reference: Optional[List[float]] = None
    created_by: Optional[uuid.UUID] = None
    project_id: Optional[uuid.UUID] = None
    team_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    meta_data: Dict[str, Any]
    status: str

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }


class MemorySearchRequest(BaseModel):
    """
    Payload schema for query text vector searches.
    """
    query: str = Field(..., description="Text query to search for using cosine similarity match.")
    team_id: uuid.UUID = Field(..., description="The team tenant context boundary for filtering.")
    limit: int = Field(10, gt=0, le=100, description="Max result count to return.")
    threshold: float = Field(0.7, ge=0.0, le=1.0, description="Minimum cosine similarity matching cutoff.")
