from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_projects():
    """
    Placeholder endpoint to retrieve projects.
    """
    return {"message": "List projects route is registered."}
