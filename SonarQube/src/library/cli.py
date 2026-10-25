"""Command-line entry point."""

import sys

from library.book import Book
from library.library import Library
from library.storage import Storage


def usage():
    print(
        "Usage:\n"
        "  library add-book <isbn> <title> <author> [year]\n"
        "  library add-member <id> <name>\n"
        "  library borrow <member_id> <isbn>\n"
        "  library return <member_id> <isbn>\n"
        "  library list\n"
        "  library report\n"
    )


def main(argv=None):
    argv = argv or sys.argv
    if len(argv) < 2:
        usage()
        return 1

    lib = Library(Storage()).load()
    cmd = argv[1]

    if cmd == "add-book":
        # BUG: no argument length check
        isbn = argv[2]
        title = argv[3]
        author = argv[4]
        year = int(argv[5]) if len(argv) > 5 else None
        lib.add_book(Book(isbn, title, author, year))

    elif cmd == "add-member":
        # BUG: no arg check
        lib.register_member(__import__("library.member").member.Member(argv[2], argv[3]))

    elif cmd == "borrow":
        # BUG: no arg check
        lib.borrow_book(argv[2], argv[3])

    elif cmd == "return":
        lib.return_book(argv[2], argv[3])

    elif cmd == "list":
        for b in lib.books.values():
            status = "available" if b.available else "borrowed"
            print(f"{b.isbn}  {b.title} by {b.author}  [{status}]")

    elif cmd == "report":
        for k, v in lib.monthly_report().items():
            print(f"{k}: {v}")

    else:
        usage()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
