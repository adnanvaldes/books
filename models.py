from dataclasses import dataclass, asdict, replace
from datetime import date
from enum import Enum
from typing import Dict, Any


class BookFormat(Enum):
    PRINT = "print"
    EBOOK = "ebook"
    AUDIO = "audiobook"


@dataclass
class Book:
    id: int | None
    title: str
    author: str
    format: BookFormat
    isbn: str | None
    pages: int | None
    runtime: int | None  # time measured in minutes
    start_date: date | None
    finish_date: date | None = None

    def copy(self, **changes: Any) -> "Book":
        return replace(self, **changes)

    def finish(self):
        self.finish_date = date.today()

    def is_finished(self):
        return self.finish_date is not None

    def validate(self):
        if self.format in (BookFormat.PRINT, BookFormat.EBOOK) and not self.pages:
            raise ValueError(f"{self.format.value} must have page count")

        if self.format == BookFormat.AUDIO and not self.runtime:
            raise ValueError("Audiobook must have runtime")

    def to_dict(self) -> dict:
        book = asdict(self)
        book["format"] = self.format.value
        book["start_date"] = self.start_date.isoformat() if self.start_date else None
        book["finish_date"] = self.finish_date.isoformat() if self.finish_date else None
        return book

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Book":
        if "format" in data and isinstance(data["format"], str):
            data["format"] = BookFormat(data["format"])
        for d in ["start_date", "finish_date"]:
            if data.get(d) and isinstance(data[d], str):
                data[d] = date.fromisoformat(data[d])
        return cls(**data)

    def __str__(self):
        return f"{self.title} [{self.author}]\t{self.is_finished()}"

    def __copy__(self):
        return self.copy()
