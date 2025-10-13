# Book Tracker CLI Design Document

## Data Fields

| SN | Title | Author | Format | P.date | Pagecount | Runtime | S.date | E.date |
| -- | ----- | ------ | ------ | ------ | --------- | ------- | ------ | ------ |
|    |       |        |        |        |           |         |        |        |
|    |       |        |        |        |           |         |        |        |

**Notes:**

* **Title** and **Format** are compulsory.
* Other fields can be auto-suggested using an LLM and confirmed by the user.
* **Start date (S.date)** defaults to `now`.
* **End date (E.date)** defaults to `None`.

---

## Features

### 1. Basics

```
book --delete "Title"
book --finish        # Updates the E.date to today
book --import        # Import entries
book --export <format>
book --edit --<column_name> "value_to_add"
```

---

### 2. Adding a Book

**Full command example:**

```
book --add --title "The Stranger" --author "Albert Camus" --format "Physical"
```

**Interactive mode:**

```
book --add

1. What is the title of the book?
2. What is the format of the book? (choose one)
   a. Physical
   b. Audiobook
   c. E-book

Would you like to autocomplete the rest of the entry? (Y/N)
if Y:
    - Use LLM to fill remaining fields
    - Verify with user
else:
    - Ask remaining fields one by one (Author, Publication date, Page count, Runtime, etc.)
```

**Partial command example:**

```
book --add --title "The Republic" --format "E-book"
```

* CLI will continue interactively, asking for missing fields.
* Optional: `--autoupdate` flag will allow LLM to fill remaining fields automatically.

---

### 3. Listing Books

```
book --list                       # List all books
book --list -a "author name"       # Filter by author
book --list -g "genre"             # Filter by genre
book --list -f "format"            # Filter by format
```

**Multi-level filtering example:**

```
book --list -a "Camus" -f "Audiobook" -g "Fiction"
```

**Sorting options:**

```
book --list --sort                # Default: A-Z by title
book --list --sort -pc            # By page count
book --list --sort -date          # By publication date
book --list --sort -S.date        # By start date
```

**Advanced example:**

```
book --list -a "Camus" -f "Audiobook" -g "Fiction" --sort -pc
```

---

### 4. Recap / Analytics

```
book --recap -a "author_name" -i "[weeks|months|years]"
```

**Example output:**

```
Recap for books by Author: Albert Camus in the past 30 days
===========================================================
Books read: 3
Finished books: 2
Pending books: 1
Total page count: 820
Average page count: 273
Average days to finish a book: 5
Max days taken to finish a book: 7 (The Stranger)
```

---

### 5. Future Features

1. **$EDITOR -> YAML:**

   * Export entries as YAML files
   * Editable in any editor and reloadable into CLI

---

### 6. Implementation Notes

* **Backend:** SQL database
* **Language:** Python
* **Libraries:** Standard library only
* **Interface:** CLI
