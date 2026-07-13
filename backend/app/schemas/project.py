import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ProjectBase(BaseModel):
    """Base schema for project context."""
    name: str
    description: Optional[str] = None
    team_id: uuid.UUID

class ProjectCreate(ProjectBase):
    """Schema for project creation request."""
    pass

class ProjectResponse(ProjectBase):
    """Schema representing project details response."""
    id: uuid.UUID
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
