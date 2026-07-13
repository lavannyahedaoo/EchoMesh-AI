import json
import asyncio
import random
from typing import List, Optional, Any
import boto3
from app.memory.interfaces import IEmbeddingService
from app.core.config import settings

class MockEmbeddingService(IEmbeddingService):
    """
    Mock implementation of IEmbeddingService for local development and offline environments.
    Generates deterministic pseudo-random 1536-dimensional embedding vectors.
    """

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generates a deterministic 1536-dimensional mock embedding for a given text.
        """
        state = random.Random(text)
        # Generate 1536 floats normalized roughly between -1.0 and 1.0
        return [state.uniform(-1.0, 1.0) for _ in range(1536)]

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generates a batch of mock embeddings.
        """
        return [await self.generate_embedding(t) for t in texts]


class BedrockEmbeddingService(IEmbeddingService):
    """
    Production implementation of IEmbeddingService that calls AWS Bedrock
    for vectorizing text using models such as Amazon Titan Text Embeddings V2.
    """

    def __init__(self, client: Optional[Any] = None):
        """
        Initializes the Bedrock client.
        """
        self.model_id = settings.BEDROCK_EMBEDDING_MODEL
        
        # Configure Boto3 connection parameters
        connection_kwargs = {
            "service_name": "bedrock-runtime",
            "region_name": settings.AWS_REGION
        }
        
        if settings.AWS_ACCESS_KEY_ID:
            connection_kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
        if settings.AWS_SECRET_ACCESS_KEY:
            connection_kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
            
        self.client = client or boto3.client(**connection_kwargs)

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Requests the vector embedding representation for a text chunk from AWS Bedrock.
        """
        body = json.dumps({
            "inputText": text,
            "dimensions": 1536,
            "normalize": True
        })

        # AWS SDK client calls are blocking synchronous I/O operations.
        # We run the invoke_model call in a thread pool executor to keep it async-safe.
        response = await asyncio.to_thread(
            self.client.invoke_model,
            body=body,
            modelId=self.model_id,
            accept="application/json",
            contentType="application/json"
        )
        
        response_body = json.loads(response.get("body").read())
        return response_body.get("embedding")

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Requests vector embeddings for a batch of text chunks concurrently.
        """
        tasks = [self.generate_embedding(text) for text in texts]
        return await asyncio.gather(*tasks)


def get_embedding_service() -> IEmbeddingService:
    """
    Factory function to retrieve the active embedding service implementation
    based on the current environment configuration.
    """
    # Use mock service for local development, tests, or offline profiles
    if settings.APP_ENV in ("local", "dev", "test"):
        return MockEmbeddingService()
        
    return BedrockEmbeddingService()
