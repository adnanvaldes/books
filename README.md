# Books CLI
`Books` is a command-line tool for managing a personal book collection. The current version has support for managing book records in a SQLite database - includes adding, editing, listing, and marking books as finished.

The architecture of the tool has the following principles (generally following domain-driven development and SOLID design patterns):

- Uses only the Python standard library - no third-party dependencies. Every Python version starting with Python 3.10 should work.
- The `Book` [model](https://github.com/adnanvaldes/books/blob/master/models.py) represents the fundamental domain attributes; data that describes a book independently of anything else.
- The `Library` [class](https://github.com/adnanvaldes/books/blob/master/library.py) encapsulates business logic. It is a logical layer that abstracts away persistence backends, allowing it to be modified for other systems (such as CSV, PSQL, etc)

This separation allows for UI and persistence logic to be modified independently. For example, the current CLI interface could easily be replaced with a REST API, a TUI, or a Discord bot — all using the same Library layer.

<img width="601" height="626" alt="books_welcome" src="https://github.com/user-attachments/assets/2e794b4b-f5e4-4fda-9e1c-43ce1df0d45f" />

---

## Features

- Add new books to your collection with metadata (format, author, start/finish dates, etc.)
- List all books or filter by completion statuspyp
- Edit or delete existing entries
- Mark books as finished or unfinished
---

## Usage

To use the tool, ensure you have Python >= 3.10 and `git` installed. Then:

```bash
# Get the source code
git clone https://github.com/adnanvaldes/books.git
cd books

# Run the app via python
python app.py

# If you prefer to run the file directly:
chmod +x ./app.py
./app.py
```

This will drop you into the welcome screen of the program. You can then run any of the commands provided by the app API (or type `-h` for help). Some examples:

```bash
# Add a book
books add --title "Dune" --author "Frank Herbert" --format print

# List books
books list

# Mark a book as finished using short flags
books edit -t "Dune" -fd 2024-06-01

# Delete a book
books delete -t "Dune"
```

Books are stored in a local SQLite database (`books.db` by default).

### Docker / Podman

You can also use Docker or Podman to run the app, using the provided Dockerfile. The container image uses `python:3.13-slim` and nothing else, so building the image should be relatively quick:

```bash
# Clone the repository
git clone https://github.com/adnanvaldes/books.git
cd books

# Build the image
## With Podman
podman build -t books-cli . # Or whatever name you want after `-t`
## With Docker
docker build -t books-cli .


# Run the image
## With Podman
podman run -it books-cli    # The container must run in interactive mode for the app to work
## With Docker
docker run -it books-cli
```
Note that to persist the database, you have to mount the `/app` directory inside the container, else the `books.db` file will be as ephemeral as the container itself. Do to so, modify the `run` command as follows:

```bash
podman run -it -v </path/to/your/local/database>:/app books-cli
```

This will use a `bind mount` to map a specific directory to the container's `/app` directory. Note that you can also specify a specific `books.db` file as part of the bind mount, but neither Docker nor Podman will create the file (they will only create directories), so make sure it exists before running the container.

---

## Development

This provect uses [uv](https://github.com/astral-sh/uv) for environment management.

### Setup

Clone the repository and test that the program runs:

```bash
git clone https://github.com/adnanvaldes/books.git
cd books
uv run app.py
```

Alternatively, use `podman` or `docker`, see [Docker / Podman](https://github.com/adnanvaldes/books#docker--podman).

Making modifications after that should be relatively straight-forward. The primary files are:
- `app.py`: This is the UI layer. The file defines a few "actions" via aptly named functions, establishes a command-line parser with `argparse`, and enters a loop to actually run the commands. This is the Views of the Model-View-Controller framework.
- `library.py`: Any command called from `app.py` leads here. This file is the logic and translation alyer between the UI and the database. All validation should happen here. In web-development terminology this is the Controller in the Model-View-Controller framework.
- `models.py`: includes a Book definition that is used by the Library and the Repository. Basically it establishes a common set of data that allows both parts of the system to talk to each other.
- `repository.py`: is the persistence layer. The job of the repositories is simply to store and retrieve data as requested by the Library.

Note: All type hints and dataclasses require Python 3.10+ due to the use of PEP 604 union syntax (int | None).
