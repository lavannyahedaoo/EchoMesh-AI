from typing import List, Any, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.user import Team

class TeamRepository(BaseRepository[Team, Any, Any]):
    """
    Team Repository handling CRUD queries for Organization workspaces / Teams.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(Team)
        self.db = db

    async def get(self, id: UUID, **kwargs: Any) -> Optional[Team]:
        """
        Retrieves a single team by its UUID.
        """
        result = await self.db.execute(select(Team).where(Team.id == id))
        return result.scalar_one_or_none()

    async def get_multi(self, skip: int = 0, limit: int = 100, **kwargs: Any) -> List[Team]:
        """
        Retrieves multiple teams with pagination offsets.
        """
        result = await self.db.execute(select(Team).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, obj_in: Any, **kwargs: Any) -> Team:
        """
        Creates and inserts a new team context.
        """
        if isinstance(obj_in, dict):
            db_obj = Team(**obj_in)
        else:
            db_obj = Team(**obj_in.model_dump())
            
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def update(self, db_obj: Team, obj_in: Any, **kwargs: Any) -> Team:
        """
        Updates properties of a team.
        """
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def remove(self, id: UUID, **kwargs: Any) -> Optional[Team]:
        """
        Removes a team container.
        """
        db_obj = await self.get(id)
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.flush()
        return db_obj
