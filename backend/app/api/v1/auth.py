from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
async def login():
    """
    Placeholder endpoint for user login.
    """
    return {"message": "Login route is registered."}

@router.post("/register")
async def register():
    """
    Placeholder endpoint for user registration.
    """
    return {"message": "Register route is registered."}
