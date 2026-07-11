from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.logging import setup_logging

# Initialize logging framework
setup_logging()

app = FastAPI(
    title="EchoMesh AI API",
    description="The AI Memory Operating System for teams API service.",
    version="1.0.0",
)

# Set up CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register central API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "app": "EchoMesh AI Backend Engine",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }
