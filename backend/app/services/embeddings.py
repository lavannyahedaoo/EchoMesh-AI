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


class LocalEmbeddingService(IEmbeddingService):
    """
    Local implementation of IEmbeddingService using sentence-transformers (all-MiniLM-L6-v2)
    with zero-padding to keep vector dimensions consistent at 1536.
    """

    def __init__(self, target_dim: int = 1536):
        self.target_dim = target_dim
        self._model = None

    @property
    def model(self):
        if self._model is None:
            # Lazy import to avoid loading heavy modules if not used immediately
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
        return self._model

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generates a 384-dimensional embedding and pads it to 1536 dimensions.
        """
        # sentence-transformers encode is synchronous. We run in a thread pool executor.
        embeddings = await asyncio.to_thread(self.model.encode, [text])
        vector = embeddings[0].tolist()
        return self._pad_vector(vector)

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generates a batch of local embeddings, each padded to 1536 dimensions.
        """
        if not texts:
            return []
        embeddings = await asyncio.to_thread(self.model.encode, texts)
        return [self._pad_vector(v.tolist()) for v in embeddings]

    def _pad_vector(self, vector: List[float]) -> List[float]:
        if len(vector) >= self.target_dim:
            return vector[:self.target_dim]
        return vector + [0.0] * (self.target_dim - len(vector))


class DynamicEmbeddingService(IEmbeddingService):
    """
    Dynamic embedding provider that decides which model and service to call
    depending on configuration, environment variables, and runtime availability.
    """

    def __init__(self):
        self.bedrock_service = None
        self.local_service = None
        self.mock_service = MockEmbeddingService()
        self._use_fallback = False

        # Determine if we should attempt AWS Bedrock
        aws_key = settings.AWS_ACCESS_KEY_ID
        aws_secret = settings.AWS_SECRET_ACCESS_KEY
        
        has_credentials = bool(aws_key and aws_secret)
        # Avoid using mock credentials as real credentials
        if has_credentials and ("mock" in aws_key.lower() or "mock" in aws_secret.lower()):
            has_credentials = False

        if has_credentials:
            try:
                self.bedrock_service = BedrockEmbeddingService()
                print("DynamicEmbeddingService: AWS credentials detected. Initialized Bedrock runtime.")
            except Exception as e:
                print(f"DynamicEmbeddingService: Failed to initialize Bedrock client: {e}. Falling back to local.")
                self._use_fallback = True
        else:
            print("DynamicEmbeddingService: AWS credentials missing. Defaulting to local sentence-transformers.")
            self._use_fallback = True

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generates embedding using Bedrock if available, else local sentence-transformers,
        with mock service as the final absolute fallback.
        """
        if not self._use_fallback and self.bedrock_service:
            try:
                return await self.bedrock_service.generate_embedding(text)
            except Exception as e:
                print(f"DynamicEmbeddingService: AWS Bedrock call failed: {e}. Falling back to local engine.")
                self._use_fallback = True

        # Fallback to Local Sentence-Transformers
        try:
            if self.local_service is None:
                self.local_service = LocalEmbeddingService()
            return await self.local_service.generate_embedding(text)
        except Exception as e:
            print(f"DynamicEmbeddingService: Local sentence-transformers failed: {e}. Falling back to deterministic Mock engine.")
            return await self.mock_service.generate_embedding(text)

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generates a batch of embeddings using the active provider with fallbacks.
        """
        if not self._use_fallback and self.bedrock_service:
            try:
                return await self.bedrock_service.generate_embeddings_batch(texts)
            except Exception as e:
                print(f"DynamicEmbeddingService: AWS Bedrock batch call failed: {e}. Falling back to local engine.")
                self._use_fallback = True

        # Fallback to Local Sentence-Transformers
        try:
            if self.local_service is None:
                self.local_service = LocalEmbeddingService()
            return await self.local_service.generate_embeddings_batch(texts)
        except Exception as e:
            print(f"DynamicEmbeddingService: Local sentence-transformers batch failed: {e}. Falling back to deterministic Mock engine.")
            return await self.mock_service.generate_embeddings_batch(texts)


# Keep a singleton instance of the dynamic service to reuse initialized clients/models
_dynamic_embedding_service_instance = None

def get_embedding_service() -> IEmbeddingService:
    """
    Factory function to retrieve the active embedding service implementation
    based on the current environment configuration.
    
    Returns a unified DynamicEmbeddingService that manages AWS Bedrock connectivity
    and local/mock fallbacks gracefully.
    """
    global _dynamic_embedding_service_instance
    if _dynamic_embedding_service_instance is None:
        _dynamic_embedding_service_instance = DynamicEmbeddingService()
    return _dynamic_embedding_service_instance
