from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.memory import Memory, MemoryLink

class MemoryRepository(BaseRepository[Memory, Any, Any]):
    """
    Memory Repository responsible for handling:
    - Standard relational CRUD for Memories and Links.
    - Vector cosine similarity queries on Titan 1536-dim embeddings.
    - Common Table Expression (CTE) SQL graph traversals to fetch linked contexts.
    """

    def __init__(self, db: AsyncSession):
        super().__init__(Memory)
        self.db = db

    async def get(self, id: UUID, **kwargs: Any) -> Optional[Memory]:
        """
        Retrieves a single memory node by its primary key UUID.
        """
        result = await self.db.execute(select(Memory).where(Memory.id == id))
        return result.scalar_one_or_none()

    async def get_multi(self, skip: int = 0, limit: int = 100, **kwargs: Any) -> List[Memory]:
        """
        Retrieves multiple memory records with support for offset pagination.
        """
        result = await self.db.execute(select(Memory).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, obj_in: Any, **kwargs: Any) -> Memory:
        """
        Inserts a new memory row. obj_in can be a dictionary or a schema model.
        """
        if isinstance(obj_in, dict):
            db_obj = Memory(**obj_in)
        else:
            db_obj = Memory(**obj_in.model_dump())
            
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def update(self, db_obj: Memory, obj_in: Any, **kwargs: Any) -> Memory:
        """
        Updates fields of an existing memory row.
        """
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def remove(self, id: UUID, **kwargs: Any) -> Optional[Memory]:
        """
        Deletes a single memory by ID.
        """
        db_obj = await self.get(id)
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.flush()
        return db_obj

    async def search_vector_similarity(
        self, 
        embedding: List[float], 
        limit: int = 10, 
        threshold: float = 0.7,
        team_id: Optional[UUID] = None
    ) -> List[Memory]:
        """
        Executes a vector similarity query against the CockroachDB vector columns.
        """
        # Convert the float array input to vector format representation '[x1, x2, ...]'
        embedding_str = "[" + ",".join(map(str, embedding)) + "]"
        
        # Compute distance expression using pgvector distance operator (<=>)
        distance_expr = text("CAST(embedding_reference AS vector) <=> CAST(:embedding AS vector) AS distance")
        distance_order = text("CAST(embedding_reference AS vector) <=> CAST(:embedding AS vector)")
        
        # Query selection containing both Memory object and distance column
        query = select(Memory, distance_expr).where(Memory.embedding_reference.isnot(None))
        
        if team_id:
            query = query.where(Memory.team_id == team_id)
            
        # Order by distance ascending (closest first)
        query = query.order_by(distance_order)
        query = query.limit(limit)
        
        # Log SQL query executed
        compiled_query = str(query.compile(compile_kwargs={"literal_binds": True}))
        print(f"--- DEBUG SEARCH: SQL EXECUTED ---\n{compiled_query}\n----------------------------------")
        print(f"DEBUG SEARCH: Generated query embedding length: {len(embedding)}")
        
        result = await self.db.execute(query, {"embedding": embedding_str})
        rows = result.all()
        
        rows_before = len(rows)
        print(f"DEBUG SEARCH: Number of rows before threshold filtering: {rows_before}")
        
        # Filter and compute similarity scores: similarity = 1.0 - distance
        all_memories = []
        filtered_memories = []
        for idx, row in enumerate(rows):
            memory_obj = row[0]
            distance = row[1]
            similarity = 1.0 - distance
            print(f"DEBUG SEARCH: Row {idx + 1}: Title='{memory_obj.title}', Cosine Distance={distance:.4f}, Cosine Similarity={similarity:.4f}")
            
            all_memories.append(memory_obj)
            if similarity >= threshold:
                filtered_memories.append(memory_obj)
                
        rows_after = len(filtered_memories)
        print(f"DEBUG SEARCH: Number of rows after threshold filtering: {rows_after}")
        
        # Requirement: "Return the top matches before applying the threshold for debugging."
        return all_memories

    async def fetch_linked_memory_graph(
        self, 
        root_memory_id: UUID, 
        max_depth: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Executes a recursive CTE (Common Table Expression) SQL query.
        
        Traverses the `memory_links` adjacency table to find all upstream and 
        downstream dependencies within the maximum hop depth limit.
        """
        cte_sql = text("""
            WITH RECURSIVE graph_cte(source_id, target_id, link_type, depth) AS (
                SELECT source_id, target_id, link_type, 1 AS depth
                FROM memory_links
                WHERE source_id = :root_id OR target_id = :root_id
                
                UNION ALL
                
                SELECT ml.source_id, ml.target_id, ml.link_type, depth + 1
                FROM memory_links ml
                JOIN graph_cte g ON ml.source_id = g.target_id OR ml.target_id = g.source_id
                WHERE depth < :max_depth
            )
            SELECT DISTINCT source_id, target_id, link_type, depth FROM graph_cte
        """)
        
        result = await self.db.execute(cte_sql, {"root_id": root_memory_id, "max_depth": max_depth})
        
        graph_edges = []
        for row in result.all():
            graph_edges.append({
                "source_id": row.source_id,
                "target_id": row.target_id,
                "link_type": row.link_type,
                "depth": row.depth
            })
            
        return graph_edges

    async def create_memory_link(
        self, 
        source_id: UUID, 
        target_id: UUID, 
        link_type: str, 
        description: Optional[str] = None
    ) -> MemoryLink:
        """
        Establishes a directed link edge between two memory nodes in the database.
        """
        link = MemoryLink(
            source_id=source_id,
            target_id=target_id,
            link_type=link_type,
            description=description
        )
        self.db.add(link)
        await self.db.flush()
        return link
