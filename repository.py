from abc import ABC, abstractmethod
from typing import List


from models import Book


class Repository(ABC):

    @abstractmethod
    def init(self) -> None:
        """Create underlying storage structure"""
        pass

    @abstractmethod
    def save(self, book: Book) -> None:
        """Insert a book record"""
        pass

    @abstractmethod
    def list(self, **filters) -> List[Book]:
        """
        List all books matching filters
        Args:
            - from : date
            - to   : date (defaults to now())
            - Book fields
        """
        pass

    @abstractmethod
    def update(self, **kwargs) -> None:
        """Update one or more fields for matching records"""
        pass

    @abstractmethod
    def delete(self, **kwargs) -> None:
        """Delete matching records"""
        pass
