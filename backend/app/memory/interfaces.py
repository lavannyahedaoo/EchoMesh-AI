from typing import List, Dict, Any, Optional
from uuid import UUID
from abc import ABC, abstractmethod

class IMemoryChunker(ABC):
    """
    Interface for parsing and partition-chunking documents and meeting transcripts.
    """
    
    @abstractmethod
    def split_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """
        Splits a text payload into smaller, semantic chunks for vectorization.
        """
        pass


class IEmbeddingService(ABC):
    """
    Interface for interacting with vectorizers (like Amazon Titan v2).
    """

    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Requests the vector embedding representation for a text chunk.
        """
        pass

    @abstractmethod
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Requests a batch of vector embeddings.
        """
        pass


class IMemoryGraphProcessor(ABC):
    """
    Interface representing cognitive link operations.
    """

    @abstractmethod
    async def analyze_and_suggest_links(
        self, 
        new_memory: Dict[str, Any], 
        candidate_memories: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Analyzes a new memory context block against candidates to identify 
        relationships (e.g. references, supersedes) using LLM reasoning.
        """
        pass
