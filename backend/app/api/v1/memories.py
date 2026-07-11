from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_memories():
    """
    Placeholder endpoint to retrieve a list of memories.
    """
    return {"message": "List memories route is registered."}

@router.post("/")
async def create_memory():
    """
    Placeholder endpoint to ingest/create a new memory node.
    """
    return {"message": "Create memory route is registered."}

@router.get("/{memory_id}")
async def get_memory(memory_id: str):
    """
    Placeholder endpoint to fetch a single memory by ID.
    """
    return {"message": f"Fetch memory {memory_id} route is registered."}
