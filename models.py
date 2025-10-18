from dataclasses import dataclass, asdict, replace
from datetime import date
from enum import Enum
from typing import Dict, Any


class BookFormat(Enum):
    PRINT = "print"
    EBOOK = "ebook"
    AUDIO = "audio"


@dataclass
class Book:
    id: int | None
    title: str
    author: str
    format: BookFormat
    isbn: str | None = None
    pages: int | None = None
    runtime: int | None = None  # time measured in minutes
    start_date: date | None = None
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
        """
        FORMAT | TITLE | AUTHOR | FINISHED | METADATA
        (BOOK ) Dune [Frank Herbert]  YES   {412p, s:2024-05-01, e:2024-05-28}
        """
        fmt = f"({self.format.value.upper()})"
        title = f"{self.title[:24]:<24}"
        author = f"[{self.author[:16]:<16}]"
        finished = "Y" if self.is_finished() else "N"

        details = []
        if self.pages:
            details.append(f"{self.pages}p")
        elif self.runtime:
            hours, minutes = self.runtime // 60, self.runtime % 60
            details.append(f"{hours}h{minutes:02d}")

        if self.start_date:
            details.append(f"s:{self.start_date.isoformat()}")
        if self.finish_date:
            details.append(f"e:{self.finish_date.isoformat()}")

        metadata = f"{{{', '.join(details)}}}" if details else ""
        return f"{fmt}{title}{author}{finished}{details}"

    def __copy__(self):
        return self.copy()
