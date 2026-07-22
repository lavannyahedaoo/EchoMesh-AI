import asyncio
import os
import sys

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.embeddings import get_embedding_service, DynamicEmbeddingService  # type: ignore

async def main():
    print("--- TESTING DYNAMIC EMBEDDING FLOW ---")
    
    # 1. Get the embedding service
    service = get_embedding_service()
    print(f"Embedding service retrieved: {type(service)}")
    assert isinstance(service, DynamicEmbeddingService), "Service should be an instance of DynamicEmbeddingService"
    
    # 2. Test single text embedding generation
    text = "Hello, testing the EchoMesh AI dynamic embedding service fallback mechanism."
    print(f"\nGenerating embedding for text: '{text}'")
    
    try:
        vector = await service.generate_embedding(text)
        print("Embedding generation successful!")
        print(f"Embedding vector dimension: {len(vector)}")
        print(f"First 5 elements of vector: {vector[:5]}")
        print(f"Last 5 elements of vector: {vector[-5:]}")
        assert len(vector) == 1536, f"Expected 1536 dimensions, got {len(vector)}"
    except Exception as e:
        print(f"ERROR generating single embedding: {e}")
        
    # 3. Test batch text embedding generation
    texts = [
        "First test memory chunk.",
        "Second test memory chunk for batching.",
        "Third chunk."
    ]
    print(f"\nGenerating embeddings for batch of {len(texts)} texts...")
    
    try:
        vectors = await service.generate_embeddings_batch(texts)
        print("Batch embedding generation successful!")
        print(f"Number of vectors returned: {len(vectors)}")
        for idx, vec in enumerate(vectors):
            print(f"Vector {idx + 1} dimension: {len(vec)}")
            assert len(vec) == 1536, f"Expected 1536 dimensions, got {len(vec)}"
    except Exception as e:
        print(f"ERROR generating batch embeddings: {e}")

if __name__ == "__main__":
    asyncio.run(main())
