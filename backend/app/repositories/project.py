from typing import List, Any, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.project import Project

class ProjectRepository(BaseRepository[Project, Any, Any]):
    """
    Project Repository handling CRUD queries for projects grouped under specific teams.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(Project)
        self.db = db

    async def get(self, id: UUID, **kwargs: Any) -> Optional[Project]:
        """
        Retrieves a single project by UUID.
        """
        result = await self.db.execute(select(Project).where(Project.id == id))
        return result.scalar_one_or_none()

    async def get_multi(self, skip: int = 0, limit: int = 100, **kwargs: Any) -> List[Project]:
        """
        Retrieves multiple projects with offset pagination.
        """
        result = await self.db.execute(select(Project).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_team_projects(self, team_id: UUID) -> List[Project]:
        """
        Retrieves all projects belonging to a specific team context.
        """
        result = await self.db.execute(select(Project).where(Project.team_id == team_id))
        return list(result.scalars().all())

    async def create(self, obj_in: Any, **kwargs: Any) -> Project:
        """
        Creates and inserts a new project.
        """
        if isinstance(obj_in, dict):
            db_obj = Project(**obj_in)
        else:
            db_obj = Project(**obj_in.model_dump())
            
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def update(self, db_obj: Project, obj_in: Any, **kwargs: Any) -> Project:
        """
        Updates a project's details.
        """
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def remove(self, id: UUID, **kwargs: Any) -> Optional[Project]:
        """
        Deletes a project.
        """
        db_obj = await self.get(id)
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.flush()
        return db_obj
