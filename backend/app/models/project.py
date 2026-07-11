import uuid
from datetime import datetime
from typing import List
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.utils.helpers import get_utc_now

class Project(Base):
    """
    Represents a specific project workspace context grouped under a Team.
    """
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)

    # Relationships
    team: Mapped["Team"] = relationship(back_populates="projects")
    memories: Mapped[List["Memory"]] = relationship(back_populates="project", cascade="all, delete-orphan")
