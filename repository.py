from abc import ABC, abstractmethod
from typing import List, Any
import sqlite3

from models import Book


class Repository(ABC):

    @abstractmethod
    def __init__(self) -> None:
        """Create underlying storage structure"""
        pass

    @abstractmethod
    def save(self, book: Book) -> None:
        """Insert a book record"""
        pass

    @abstractmethod
    def list(self, **identifiers) -> List[Book]:
        """
        List all books matching filters
        Args:
            - from : date
            - to   : date (defaults to now())
            - Book fields
        """
        pass

    @abstractmethod
    def update(self, book: Book) -> None:
        """Update one or more fields for matching records"""
        pass

    @abstractmethod
    def delete(self, book: Book) -> None:
        """Delete matching records"""
        pass


class SQLRepository(Repository):
    def __init__(self, db_path="books.db"):
        self.conn = sqlite3.connect(db_path)  # creates or connects with the file
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
			CREATE TABLE IF NOT EXISTS books (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT NOT NULL,
				author TEXT NOT NULL,
				format TEXT NOT NULL,
				isbn TEXT,
				pages INTEGER,
				runtime INTEGER,
				start_date TEXT,
				finish_date TEXT
			);
		"""
        )  # we are actually createing the table if it doesnot exist and thereason why datatypes are different here than the models  is because models are purely pythonic and this is for SQL initilization.

    def save(self, book: Book) -> Book:
        query = """
            INSERT INTO books (title, author, format, isbn, pages, runtime, start_date, finish_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(
            query,
            (
                book.title,
                book.author,
                book.format.value,
                book.isbn,
                book.pages,
                book.runtime,
                book.start_date.isoformat() if book.start_date else None,
                book.finish_date.isoformat() if book.finish_date else None,
            ),
        )
        self.conn.commit()
        book.id = self.cursor.lastrowid
        return book

    def update(self, book: Book) -> Book:
        if book.id is None:
            raise ValueError("Cannot update a book without an ID")

        query = """
            UPDATE books
            SET title=?, author=?, format=?, isbn=?, pages=?, runtime=?, start_date=?, finish_date=?
            WHERE id=?
        """
        self.cursor.execute(
            query,
            (
                book.title,
                book.author,
                book.format.value,
                book.isbn,
                book.pages,
                book.runtime,
                book.start_date.isoformat() if book.start_date else None,
                book.finish_date.isoformat() if book.finish_date else None,
                book.id,
            ),
        )
        self.conn.commit()
        return book

    def delete(self, book: Book) -> None:
        if book.id is None:
            raise ValueError("Cannot delete a book without an ID")
        self.cursor.execute("DELETE FROM books WHERE id=?", (book.id,))
        self.conn.commit()

    def list(self, **filters: Any) -> List[Book]:
        query = "SELECT * FROM books"
        clauses, params = [], []

        from_date = filters.pop("from_date", None)
        to_date = filters.pop("to_date", None)

        for key, value in filters.items():
            if value is not None:
                clauses.append(f"{key} = ?")
                params.append(value)

        if from_date:
            clauses.append("start_date >= ?")
            params.append(from_date)
        if to_date:
            clauses.append("finish_date <= ?")
            params.append(to_date)

        if clauses:
            query += " WHERE " + " AND ".join(clauses)

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return [Book.from_dict(dict(row)) for row in rows]
