import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import String, ForeignKey, DateTime, Integer, Float, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.utils.helpers import get_utc_now

class MemoryTag(Base):
    """
    Association table representing the many-to-many relationship between Memories and Tags.
    """
    __tablename__ = "memory_tags"

    memory_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("memories.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)


class Tag(Base):
    """
    Represents semantic labels linked to memories for quick filtering and grouping.
    """
    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)

    # Relationships
    memories: Mapped[List["Memory"]] = relationship(
        secondary="memory_tags", back_populates="tags"
    )


class MemoryLink(Base):
    """
    Represents a directed link (edge) between two Memory nodes in our memory graph.
    """
    __tablename__ = "memory_links"
    __table_args__ = (
        UniqueConstraint("source_id", "target_id", "link_type", name="uq_source_target_type"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("memories.id", ondelete="CASCADE"), index=True, nullable=False)
    target_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("memories.id", ondelete="CASCADE"), index=True, nullable=False)
    link_type: Mapped[str] = mapped_column(String(50), nullable=False) # e.g. references, supersedes, refutes, supports, blocks
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)

    # Relationships
    source: Mapped["Memory"] = relationship(foreign_keys=[source_id], back_populates="links_from")
    target: Mapped["Memory"] = relationship(foreign_keys=[target_id], back_populates="links_to")


class Memory(Base):
    """
    The Universal Memory Object.
    Represents any discrete piece of organizational knowledge stored in the OS.
    """
    __tablename__ = "memories"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    memory_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False) # e.g. decision, meeting, document, bug, task, etc.
    importance: Mapped[int] = mapped_column(Integer, default=1) # 1 (low) to 5 (critical)
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    embedding_reference: Mapped[Optional[List[float]]] = mapped_column(ARRAY(Float), nullable=True) # Titan Embeddings (1536 dim)
    
    # Context scopes
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True)
    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)
    meta_data: Mapped[Dict[str, Any]] = mapped_column("metadata", JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(50), default="active") # active, archived

    # Core Relationships
    author: Mapped[Optional["User"]] = relationship(back_populates="created_memories")
    team: Mapped["Team"] = relationship(back_populates="memories")
    project: Mapped[Optional["Project"]] = relationship(back_populates="memories")
    tags: Mapped[List[Tag]] = relationship(secondary="memory_tags", back_populates="memories")

    # Graph Relationships
    links_from: Mapped[List[MemoryLink]] = relationship(foreign_keys=[MemoryLink.source_id], back_populates="source", cascade="all, delete-orphan")
    links_to: Mapped[List[MemoryLink]] = relationship(foreign_keys=[MemoryLink.target_id], back_populates="target", cascade="all, delete-orphan")

    # Domain specific extension relationships (One-to-One)
    decision: Mapped[Optional["Decision"]] = relationship(back_populates="memory", uselist=False, cascade="all, delete-orphan")
    meeting: Mapped[Optional["Meeting"]] = relationship(back_populates="memory", uselist=False, cascade="all, delete-orphan")
    document: Mapped[Optional["Document"]] = relationship(back_populates="memory", uselist=False, cascade="all, delete-orphan")
    conversation: Mapped[Optional["Conversation"]] = relationship(back_populates="memory", uselist=False, cascade="all, delete-orphan")


class Decision(Base):
    """
    Subtype extension for decisions. Contains rationale, rejected alternatives, and approvers.
    """
    __tablename__ = "decisions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    memory_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("memories.id", ondelete="CASCADE"), unique=True, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    rejected_alternatives: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, default=list) # Title, desc, rejection_reason
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    outcome: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    memory: Mapped[Memory] = relationship(back_populates="decision")
    approver: Mapped[Optional["User"]] = relationship(back_populates="decisions")


class Meeting(Base):
    """
    Subtype extension for meetings. Stores transcript summaries and media pointers.
    """
    __tablename__ = "meetings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    memory_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("memories.id", ondelete="CASCADE"), unique=True, nullable=False)
    meeting_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    recording_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    transcript_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationships
    memory: Mapped[Memory] = relationship(back_populates="meeting")


class Document(Base):
    """
    Subtype extension for files/attachments uploaded to the storage layer.
    """
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    memory_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("memories.id", ondelete="CASCADE"), unique=True, nullable=False)
    s3_key: Mapped[str] = mapped_column(String(512), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(100), nullable=False) # mime-type
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    memory: Mapped[Memory] = relationship(back_populates="document")


class Conversation(Base):
    """
    Subtype extension representing instant messaging logs (e.g. Slack/Teams logs).
    """
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    memory_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("memories.id", ondelete="CASCADE"), unique=True, nullable=False)
    channel_name: Mapped[str] = mapped_column(String(100), nullable=False)
    platform: Mapped[str] = mapped_column(String(50), nullable=False) # e.g. slack, teams
    message_count: Mapped[int] = mapped_column(Integer, default=1)

    # Relationships
    memory: Mapped[Memory] = relationship(back_populates="conversation")
