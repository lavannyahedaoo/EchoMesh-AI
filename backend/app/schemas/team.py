import uuid
from datetime import datetime
from pydantic import BaseModel

class TeamBase(BaseModel):
    """Base schema for team context."""
    name: str

class TeamCreate(TeamBase):
    """Schema for team creation request."""
    pass

class TeamResponse(TeamBase):
    """Schema representing team details response."""
    id: uuid.UUID
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
