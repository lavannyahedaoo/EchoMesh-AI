from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectResponse
from app.utils.seeding import seed_if_empty

router = APIRouter()

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves all projects. Automatically seeds a default workspace
    if the database is currently empty.
    """
    try:
        # Check and seed if database is empty
        await seed_if_empty(db)
        
        # Query repository
        repository = ProjectRepository(db)
        projects = await repository.get_multi(skip=skip, limit=limit)
        return projects
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve projects: {str(e)}"
        )
