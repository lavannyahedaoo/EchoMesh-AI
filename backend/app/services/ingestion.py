import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.memory.interfaces import IMemoryChunker, IEmbeddingService
from app.models.memory import Memory

class IngestionService:
    """
    Service responsible for document and text ingestion.
    Coordinates content chunking, vector embedding generation, and 
    transactional persistence of memories inside CockroachDB.
    """

    def __init__(
        self, 
        db: AsyncSession, 
        chunker: IMemoryChunker, 
        embedding_service: IEmbeddingService
    ):
        self.db = db
        self.chunker = chunker
        self.embedding_service = embedding_service

    async def ingest_memory(
        self,
        title: str,
        content: str,
        memory_type: str,
        team_id: uuid.UUID,
        created_by: Optional[uuid.UUID] = None,
        project_id: Optional[uuid.UUID] = None,
        importance: int = 1,
        confidence_score: float = 1.0,
        meta_data: Optional[Dict[str, Any]] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> List[Memory]:
        """
        Accepts content, splits it into chunks, generates vector embeddings for each,
        and saves them transactionally in the database.
        
        Args:
            title (str): Base title of the memories.
            content (str): The raw text/document content to ingest.
            memory_type (str): Type classification (e.g. document, decision, meeting).
            team_id (UUID): The associated tenant workspace team.
            created_by (UUID, optional): User ID of the creator.
            project_id (UUID, optional): ID of the project container.
            importance (int): Importance rank from 1 to 5.
            confidence_score (float): Confidence classification score.
            meta_data (dict, optional): Custom JSON payload context metadata.
            chunk_size (int): Max chunk character size.
            chunk_overlap (int): Overlap character size.
            
        Returns:
            List[Memory]: List of created and saved Memory model instances.
        """
        # Slice text into chunks
        chunks = self.chunker.split_text(content, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        # If no chunks were generated (empty content), process as single empty block
        if not chunks:
            chunks = [content]

        # Generate vectors concurrently
        embeddings = await self.embedding_service.generate_embeddings_batch(chunks)

        memories_to_save: List[Memory] = []
        
        try:
            for idx, (chunk_text, chunk_vector) in enumerate(zip(chunks, embeddings)):
                # Differentiate multi-chunk memory titles
                chunk_title = f"{title} (Part {idx + 1})" if len(chunks) > 1 else title
                
                # Truncate content for summary if necessary
                summary_length = 200
                chunk_summary = chunk_text[:summary_length] + ("..." if len(chunk_text) > summary_length else "")

                memory_node = Memory(
                    title=chunk_title,
                    summary=chunk_summary,
                    content=chunk_text,
                    memory_type=memory_type,
                    importance=importance,
                    confidence_score=confidence_score,
                    embedding_reference=chunk_vector,
                    created_by=created_by,
                    project_id=project_id,
                    team_id=team_id,
                    meta_data=meta_data or {},
                    status="active"
                )
                
                self.db.add(memory_node)
                memories_to_save.append(memory_node)
                
            # Flush session to fetch database-generated fields (like memory IDs) without committing yet
            await self.db.flush()
            return memories_to_save
            
        except Exception as e:
            # Transaction boundary: Rollback entire block on failure to maintain database integrity
            await self.db.rollback()
            raise e
