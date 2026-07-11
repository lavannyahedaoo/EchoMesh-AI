from typing import Generic, TypeVar, List, Optional, Any
from uuid import UUID
from pydantic import BaseModel

# Type variables for SQLModel/SQLAlchemy Model and Pydantic Schema DTOs
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Abstract Base Repository Interface.
    
    Establishes baseline CRUD operation declarations that all domain repositories 
    (e.g., UserRepository, MemoryRepository) must implement or inherit.
    """
    
    def __init__(self, model_class: type[ModelType]):
        """
        Initializes repository with a reference to the SQLModel/SQLAlchemy class type.
        """
        self.model_class = model_class

    async def get(self, id: UUID, **kwargs: Any) -> Optional[ModelType]:
        """
        Retrieve a single entity by its UUID primary key.
        """
        raise NotImplementedError

    async def get_multi(self, skip: int = 0, limit: int = 100, **kwargs: Any) -> List[ModelType]:
        """
        Retrieve a slice of entities with pagination offsets.
        """
        raise NotImplementedError

    async def create(self, obj_in: CreateSchemaType, **kwargs: Any) -> ModelType:
        """
        Insert a new entity record into the database.
        """
        raise NotImplementedError

    async def update(self, db_obj: ModelType, obj_in: UpdateSchemaType, **kwargs: Any) -> ModelType:
        """
        Update an existing entity record with modified attributes.
        """
        raise NotImplementedError

    async def remove(self, id: UUID, **kwargs: Any) -> Optional[ModelType]:
        """
        Delete an entity record from the database.
        """
        raise NotImplementedError
