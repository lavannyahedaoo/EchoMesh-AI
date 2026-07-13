from typing import List
from app.memory.interfaces import IMemoryChunker

class MemoryChunker(IMemoryChunker):
    """
    Concrete implementation of IMemoryChunker that splits text payloads
    into smaller overlapping chunks using character-level sliding windows.
    """

    def split_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """
        Splits a text payload into smaller character chunks with a specified overlap.
        
        Args:
            text (str): The raw text payload to be chunked.
            chunk_size (int): Max character length of each chunk.
            chunk_overlap (int): Overlap character length between sequential chunks.
            
        Returns:
            List[str]: A list of text chunks.
        """
        if not text:
            return []

        if chunk_size <= 0:
            raise ValueError("chunk_size must be a positive integer.")

        if chunk_overlap < 0 or chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be non-negative and strictly less than chunk_size.")

        chunks = []
        text_len = len(text)
        start = 0

        while start < text_len:
            end = min(start + chunk_size, text_len)
            chunks.append(text[start:end])
            
            if end == text_len:
                break
                
            # Advance start by slide length (chunk_size - chunk_overlap)
            start += chunk_size - chunk_overlap

        return chunks
