from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.repositories.team import TeamRepository
from app.schemas.team import TeamResponse
from app.utils.seeding import seed_if_empty

router = APIRouter()

@router.get("/", response_model=List[TeamResponse])
async def list_teams(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves all teams. Automatically seeds a default workspace
    if the database is currently empty.
    """
    try:
        # Check and seed if database is empty
        await seed_if_empty(db)
        
        # Query repository
        repository = TeamRepository(db)
        teams = await repository.get_multi(skip=skip, limit=limit)
        return teams
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve teams: {str(e)}"
        )
