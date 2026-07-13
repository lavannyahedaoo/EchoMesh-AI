from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import Team
from app.models.project import Project

async def seed_if_empty(db: AsyncSession) -> None:
    """
    Checks if the database has any Team contexts configured. If empty,
    seeds one default Team and one default Project mapped to it.
    """
    # Query all teams
    team_query = await db.execute(select(Team))
    teams = team_query.scalars().all()
    
    if not teams:
        # Seed a sample team
        sample_team = Team(name="Sample Team Workspace")
        db.add(sample_team)
        await db.flush()  # Generate UUID
        
        # Seed a sample project linked to the team
        sample_project = Project(
            team_id=sample_team.id,
            name="Sample Project Workspace",
            description="Automatically seeded sample project for integration testing."
        )
        db.add(sample_project)
        await db.flush()
        
        # Commit to CockroachDB
        await db.commit()
