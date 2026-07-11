from typing import Dict, Any, List
from app.agents.base import BaseAgent

class MemoryAgent(BaseAgent):
    """
    Memory Agent responsible for extracting, mapping, and formatting raw text files
    or conversations into structured UniversalMemoryObject definitions.
    """

    def __init__(self, model_id: str):
        # We enforce zero temperature for structured extraction tasks to minimize hallucination
        super().__init__(model_id=model_id, temperature=0.0)

    async def run(self, input_data: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Parses raw text payload, executes the extraction prompt with Bedrock,
        and parses results matching the UniversalMemoryObject fields.
        """
        # Placeholder: will use LangChain Structured Output Parsers with Claude
        return {}


class MemoryLinkingAgent(BaseAgent):
    """
    Memory Linking Agent evaluates semantic similarity overlaps and constructs 
    directed topological relationship edges (supersedes, blocks, etc.) between nodes.
    """

    def __init__(self, model_id: str):
        super().__init__(model_id=model_id, temperature=0.1)

    async def run(self, input_data: Dict[str, Any], **kwargs: Any) -> List[Dict[str, Any]]:
        """
        Expects a payload containing the target 'new_memory' details and 
        a list of 'candidate_memories'.
        
        Returns generated connection paths with justifications.
        """
        # Placeholder: will analyze relationships and write edges to database
        return []
