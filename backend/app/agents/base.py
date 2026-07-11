from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """
    Abstract Base Class for EchoMesh AI agent workflows.
    Encapsulates interactions with Amazon Bedrock via LangChain.
    """

    def __init__(self, model_id: str, temperature: float = 0.0):
        self.model_id = model_id
        self.temperature = temperature

    @abstractmethod
    async def run(self, input_data: Any, **kwargs: Any) -> Any:
        """
        Executes the agentic workflow (prompting, execution, response schema parsing).
        """
        pass
