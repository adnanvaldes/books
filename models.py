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

    def __post_init__(self):
        if not self.format:
            raise ValueError("Format is required (e.g. print, audio, ebook)")

        if isinstance(self.format, str):
            try:
                fmt = "audio" if self.format.lower() == "audiobook" else self.format
                self.format = BookFormat(fmt.lower())
            except ValueError:
                raise ValueError(f"Invalid book format: {self.format}")

        if isinstance(self.start_date, str):
            try:
                self.start_date = date.fromisoformat(self.start_date)
            except ValueError:
                raise ValueError(f"Invalid date format: {self.start_date}")

        if isinstance(self.finish_date, str):
            try:
                self.finish_date = date.fromisoformat(self.finish_date)
            except ValueError:
                raise ValueError(f"Invalid date format: {self.finish_date}")

    def copy(self, **changes: Any) -> "Book":
        return replace(self, **changes)

    def finish(self):
        self.finish_date = date.today()

    def is_finished(self):
        return self.finish_date is not None

    def to_dict(self) -> dict:
        book = asdict(self)
        book["format"] = self.format.value
        book["start_date"] = self.start_date.isoformat() if self.start_date else None
        book["finish_date"] = self.finish_date.isoformat() if self.finish_date else None
        return book

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Book":
        if "format" in data and isinstance(data["format"], str):
            fmt = "audio" if data["format"].lower() == "audiobook" else data["format"]
            data["format"] = BookFormat(fmt.lower())

        for d in ["start_date", "finish_date"]:
            if data.get(d) and isinstance(data[d], str):
                data[d] = date.fromisoformat(data[d])
        return cls(**data)

    def __str__(self):
        """
        FORMAT | TITLE | AUTHOR | FINISHED | METADATA
        (BOOK ) Dune [Frank Herbert]  YES   {s:2024-05-01, e:2024-05-28, 412p}
        """
        fmt = f"({self.format.value.upper()})"
        title = f"{self.title[:16]:<16}"
        author = f"[{self.author[:16]:<16}]"
        finished = "Y" if self.is_finished() else "N"

        details = []
        if self.start_date:
            details.append(f"s:{self.start_date.isoformat()}")
        if self.finish_date:
            details.append(f"e:{self.finish_date.isoformat()}")

        if self.pages:
            details.append(f"{self.pages}p")
        elif self.runtime:
            hours, minutes = self.runtime // 60, self.runtime % 60
            details.append(f"{hours}h{minutes:02d}")

        metadata = f"{{{', '.join(details)}}}" if details else ""
        metadata = f"{metadata:<40}"
        return f"{fmt} {title} {author} {finished} {metadata}"

    def __copy__(self):
        return self.copy()
