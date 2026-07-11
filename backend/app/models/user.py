import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.utils.helpers import get_utc_now

class TeamMember(Base):
    """
    Association model representing the many-to-many link between Users and Teams.
    """
    __tablename__ = "team_members"

    team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role: Mapped[str] = mapped_column(String(50), default="member") # e.g. admin, member, viewer
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)

    # Relationships
    team: Mapped["Team"] = relationship(back_populates="memberships")
    user: Mapped["User"] = relationship(back_populates="team_memberships")


class User(Base):
    """
    Represents an individual user profile in EchoMesh AI.
    """
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)

    # Relationships
    team_memberships: Mapped[List[TeamMember]] = relationship(back_populates="user", cascade="all, delete-orphan")
    created_memories: Mapped[List["Memory"]] = relationship(back_populates="author")
    audit_logs: Mapped[List["AuditLog"]] = relationship(back_populates="user")
    decisions: Mapped[List["Decision"]] = relationship(back_populates="approver")


class Team(Base):
    """
    Represents an isolated organizational workspace / team context.
    """
    __tablename__ = "teams"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)

    # Relationships
    memberships: Mapped[List[TeamMember]] = relationship(back_populates="team", cascade="all, delete-orphan")
    projects: Mapped[List["Project"]] = relationship(back_populates="team", cascade="all, delete-orphan")
    memories: Mapped[List["Memory"]] = relationship(back_populates="team", cascade="all, delete-orphan")
