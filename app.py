import loadscreen
import argparse
from library import Library
from typing import Dict
from repository import SQLRepository
from datetime import date
from tabulate import tabulate
import shlex


def add(data: Dict):
    data.pop("action", None)
    print("added book entry as :", library.add(data))
    return


def edit(data: Dict):
    data.pop("action", None)
    data.pop("edit_action", None)

    identifiers = {}
    updates = {}

    for k, v in data.items():
        if v is not None:
            if k.startswith("set_"):
                field_name = k.replace("set_", "")
                updates[field_name] = v
            else:
                identifiers[k] = v
    if not updates:
        print("Error: Please specify at least one field to update using --set-* flags")
        return

    print(f"Updated entry to {library.update(updates, **identifiers)}")
    return


def delete(data: dict):
    data.pop("action", None)
    data = {key: value for key, value in data.items() if value is not None}
    library.delete(**data)
    return


def finish(data: dict):
    data.pop("action", None)
    data = {key: value for key, value in data.items() if value is not None}
    library.finish(**data)
    return


def import_():
    print("import function will be here ")
    return


def export_():
    print("Export function will be here ")
    return


def list_(data: Dict):
    data.pop("action", None)
    clean_data = {key: value for key, value in data.items() if value is not None}
    Books = library.list_(**clean_data)
    print(tabulate(Books))


def recap():
    print("recap function will be here")


def to_date(string: str) -> date:
    return date.fromisoformat(string)


def include_common_args(parser: argparse.ArgumentParser):
    parser.add_argument("-a", "--author", type=str, help="name of author")
    parser.add_argument("-t", "--title", type=str, help="name of book")
    parser.add_argument(
        "-f", "--format", type=str, help="book format (physical, e-book, audiobook)"
    )
    parser.add_argument("-i", "--isbn", type=str, help="ISBN code")
    parser.add_argument("-p", "--pages", type=int, help="number of pages")
    parser.add_argument("-r", "--runtime", type=int, help="runtime (for audiobooks)")
    parser.add_argument("-sd", "--start_date", type=to_date, help="start date")
    parser.add_argument("-fd", "--finish_date", type=to_date, help="finish date")


def add_setter_args(parser: argparse.ArgumentParser):
    parser.add_argument("-sa", "--set-author", type=str, help="new author name")
    parser.add_argument("-st", "--set-title", type=str, help="new book title")
    parser.add_argument("-sf", "--set-format", type=str, help="new format")
    parser.add_argument("-si", "--set-isbn", type=str, help="new ISBN")
    parser.add_argument("-sp", "--set-pages", type=int, help="new page count")
    parser.add_argument("-sr", "--set-runtime", type=int, help="new runtime")
    parser.add_argument("-ssd", "--set-start-date", type=to_date, help="new start date")
    parser.add_argument(
        "-sfd", "--set-finish-date", type=to_date, help="new finish date"
    )


def cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="book", description="Book manager")
    subparsers = parser.add_subparsers(dest="action", required=True)

    clear_parser = subparsers.add_parser("clear", help="Clear screen")
    add_parser = subparsers.add_parser("add", help="Add a book")
    list_parser = subparsers.add_parser("list", help="List books")
    delete_parser = subparsers.add_parser("delete", help="Delete a book")
    finish_parser = subparsers.add_parser("finish", help="Mark book as finished")
    edit_parser = subparsers.add_parser("edit", help="Edit existing book entries")

    for parse in (add_parser, list_parser, delete_parser, finish_parser, edit_parser):
        include_common_args(parse)
    add_setter_args(edit_parser)

    return parser


def main():
    loadscreen.welcome()
    print("Welcome to Books ")
    print("For help enter : books -h")
    parser = cli_parser()
    while True:
        try:
            user_input = input("> ").strip()
            if user_input in ["exit", "quit"]:
                print("\nThanks for using books")
                break
            if not user_input:
                continue
            args = parser.parse_args(shlex.split(user_input))
            command = {
                "add": add,
                "list": list_,
                "edit": edit,
                "finish": finish,
                "delete": delete,
                "import": import_,
                "export": export_,
                "recap": recap,
                "clear": loadscreen.welcome(),
            }
            func = command.get(args.action)
            # print(vars(args))
            if func:
                func(vars(args))

        except SystemExit:
            continue
        except KeyboardInterrupt:
            print("\nThanks for using books")
            break


if __name__ == "__main__":
    repository = SQLRepository()
    library = Library(repository)
    main()
