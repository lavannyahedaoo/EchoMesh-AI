from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.repositories.memory import MemoryRepository
from app.schemas.memory import MemoryIngestRequest, MemoryResponse, MemorySearchRequest
from app.services.chunker import MemoryChunker
from app.services.embeddings import get_embedding_service
from app.services.ingestion import IngestionService

router = APIRouter()

@router.post("/ingest", response_model=List[MemoryResponse], status_code=status.HTTP_201_CREATED)
async def ingest_memory(
    payload: MemoryIngestRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Ingests text/document content, chunks it semantically,
    generates vector embeddings, and stores them in the database.
    """
    chunker = MemoryChunker()
    embedding_service = get_embedding_service()
    ingestion_service = IngestionService(db, chunker, embedding_service)
    
    try:
        memories = await ingestion_service.ingest_memory(
            title=payload.title,
            content=payload.content,
            memory_type=payload.memory_type,
            team_id=payload.team_id,
            project_id=payload.project_id,
            importance=payload.importance,
            confidence_score=payload.confidence_score,
            meta_data=payload.meta_data,
            chunk_size=payload.chunk_size,
            chunk_overlap=payload.chunk_overlap
        )
        return memories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest memory content: {str(e)}"
        )


@router.post("/search", response_model=List[MemoryResponse])
async def search_memories(
    payload: MemorySearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Vector similarity search endpoint that generates query embeddings
    and executes cosine distance retrieval queries.
    """
    embedding_service = get_embedding_service()
    repository = MemoryRepository(db)
    
    try:
        # Generate the query embedding vector
        query_vector = await embedding_service.generate_embedding(payload.query)
        
        # Execute the vector matching query
        memories = await repository.search_vector_similarity(
            embedding=query_vector,
            limit=payload.limit,
            threshold=payload.threshold,
            team_id=payload.team_id
        )
        return memories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vector search execution failed: {str(e)}"
        )


@router.get("/", response_model=List[MemoryResponse])
async def list_memories(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves multiple memories with pagination offsets.
    """
    repository = MemoryRepository(db)
    memories = await repository.get_multi(skip=skip, limit=limit)
    return memories


@router.get("/{memory_id}", response_model=MemoryResponse)
async def get_memory(
    memory_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves a single memory node by its ID.
    """
    repository = MemoryRepository(db)
    memory = await repository.get(memory_id)
    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Memory with ID {memory_id} not found."
        )
    return memory
