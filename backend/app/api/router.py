from fastapi import APIRouter
from app.api.v1 import auth, memories, projects, teams

api_router = APIRouter()

# Include subdomain routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(memories.router, prefix="/memories", tags=["memories"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
