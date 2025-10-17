from typing import Dict, List, Any
import uuid
from models import Book
from repository import Repository


class NoBooksFoundError(Exception):
    """Raised when no books match the given identifiers"""

    def __init__(self, identifiers: Dict):
        self.identifiers = identifiers
        super().__init__(f"No books found matching {identifiers}")


class TooManyBooksFoundError(Exception):
    """Raise when too many books match the given identifiers"""

    def __init__(self, action: str, identifiers: Dict, books: List):
        self.action = action
        self.identifiers = identifiers
        super().__init__(
            f"Based on {identifiers}.\nCannot {action}. Please be more specific."
        )
        for book in books:
            print(book)


class NoIdentifiersError(Exception):
    """Raised when no identifiers are used in a search function"""

    def __init__(self):
        super().__init__("You must specify at least one identifier.")


class Library:

    def __init__(self, repository: Repository):
        self.repository = repository

    def add(self, data: Dict[str, Any]) -> Book:
        data['id'] = str(uuid.uuid4())
        book=Book.from_dict(data)
        book.validate()

        self.repository.save(book)
        return book

    def update(self, updates: Dict[str, Any], **identifiers: Any) -> Book:
        if not identifiers:
            raise NoIdentifiersError

        target_book = self._get_single_book_for("update", identifiers)
        updated_book = target_book.copy(**updates)
        updated_book.validate()
        self.repository.update(book=updated_book)

        return updated_book

    def finish(self, **identifiers: Any) -> Book:
        if not identifiers:
            raise NoIdentifiersError

        target_book = self._get_single_book_for("finish", identifiers)
        if target_book.is_finished():
            return target_book

        finished_book = target_book.copy()
        finished_book.finish()

        self.repository.save(finished_book)
        return finished_book

    def list_(self, **identifiers) -> List[Book]:
        if not identifiers:
            return self.repository.list()

        return self.repository.list(**identifiers)

    def preview(
        self, updates: Dict[str, Any] | None = None, **identifiers: Any
    ) -> List[Book]:
        books = self.repository.list(**identifiers)
        if not books:
            raise NoBooksFoundError(identifiers)

        if updates is None:
            return books  # If not updates are passed, presumably deletion is happening

        previews = []
        for book in books:
            preview_book = book.copy(**updates)
            preview_book.validate()
            previews.append(preview_book)
        return previews

    def delete(self, **identifiers: Any) -> None:
        if not identifiers:
            raise NoIdentifiersError

        target_book = self._get_single_book_for("delete", identifiers)
        self.repository.delete(book=target_book)

    def _get_single_book_for(self, action: str, identifiers: Dict) -> Book:
        matching_books = self.repository.list(**identifiers)

        if not matching_books:
            raise NoBooksFoundError(identifiers)

        if len(matching_books) > 1:
            raise TooManyBooksFoundError(action, identifiers, matching_books)

        return matching_books[0]
