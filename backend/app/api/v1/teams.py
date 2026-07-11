from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_teams():
    """
    Placeholder endpoint to retrieve teams.
    """
    return {"message": "List teams route is registered."}
