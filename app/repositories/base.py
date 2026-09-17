from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    """Abstract generic repository interface."""

    @abstractmethod
    def get_all(self) -> List[T]:
        """Retrieve all entity records."""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Retrieve single entity by unique identifier."""
        pass
