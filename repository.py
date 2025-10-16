from abc import ABC, abstractmethod
from typing import List,Any
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
    def update(self, book: Book, **identifiers) -> None:
        """Update one or more fields for matching records"""
        pass

    @abstractmethod
    def delete(self, **kwargs) -> None:
        """Delete matching records"""
        pass

class SQLRepository(Repository):
    def __init__(self, db_path = "books.db"):
        self.conn=sqlite3.connect(db_path)#creates or connects with the file 
        self.cursor=self.conn.cursor()
        self.init()
    
    def init(self)->None:
        self.cursor.execute("""
			CREATE TABLE books (
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
		""")#we are actually createing the table if it doesnot exist and thereason why datatypes are different here than the models  is because models are purely pythonic and this is for SQL initilization.
    def save(self,book:Book)->None:
        existing = self.cursor.execute("SELECT id FROM books WHERE id = ?", (book.id,)).fetchone()
        if existing:
            self.update(book)
        else:
            self.cursor.execute("INSERT INTO books(title,author,format,isbn,pages,runtime,start_date,finish_date) VALUES(?,?,?,?,?,?,?,?)",(
			book.title,
			book.author,
			book.format.value,  # convert Enum to string
			book.isbn,
			book.pages,
			book.runtime,
			book.start_date.isoformat() if book.start_date else None,
			book.finish_date.isoformat() if book.finish_date else None
    ))
        """
        better way to do this is 
        book_dict = book.to_dict()
		columns = ", ".join(book_dict.keys())                  # "title,author,format,isbn,..."
		placeholders = ", ".join("?" for _ in book_dict)       # "?, ?, ?, ..."
		values = list(book_dict.values())                     # ["1984", "George Orwell", "book", ...]

		cursor.execute(
			f"INSERT INTO books ({columns}) VALUES ({placeholders})",
			values
		)
	 """
            	
    # def update(self, book: Book) -> None:
    #     """Update an existing book (by id)"""
    #     if book.id is None:
    #         raise ValueError("Book must have an id to be updated")
    #     self.cursor.execute(
    #         "UPDATE books SET title = ?, author = ?, published = ? WHERE id = ?",
    #         (book.title, book.author, book.published, book.id),
    #     )
    #     self.conn.commit()

    def delete(self, book_id: int) -> None:
        """Delete a book by id"""
        self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()#this will need an update too 
        
    
    
    def list(self, **identifiers: Any) -> List[Book]:
        query="SELECT id, title, author, format, isbn, pages, runtime, start_date, finish_date FROM books"
        parms=[]
        if identifiers:
            conditions=[]
            for key,value in identifiers.items():
                conditions.append(f"{key} = ?")
                parms.append(value)
                
            query += " WHERE " + " AND ".join(conditions)
        #we use this system and not directly author={authorname} because we want to avoid maliciuos commands which may create the wrong query and also to deal with special characters.
        self.cursor.execute(query,parms)
        rows = self.cursor.fetchall()
        books = []
        for row in rows:
            book_data = {
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'format': row[3],  # Will be converted back to Enum in Book.__init__
            'isbn': row[4],
            'pages': row[5],
            'runtime': row[6],
            'start_date': row[7],  # Will be parsed in Book.__init__
            'finish_date': row[8]
        }
            books.append(Book(**book_data))
        return Book