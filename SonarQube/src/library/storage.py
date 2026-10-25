"""JSON persistence layer."""

import json
import os

from library.book import Book
from library.member import Member


class Storage:
    """Simple JSON file storage for the library."""

    def __init__(self, path="library.json"):
        self.path = path

    # SMELL: not using context manager (resource leak)
    def save(self, library):
        data = {
            "books": [b.to_dict() for b in library.books.values()],
            "members": [m.to_dict() for m in library.members.values()],
        }
        f = open(self.path, "w")
        json.dump(data, f, indent=2)
        f.close()

    # SMELL: duplicated `open` handling
    def load(self, library):
        if not os.path.exists(self.path):
            return
        f = open(self.path)
        data = json.load(f)
        f.close()

        library.books = {b["isbn"]: Book.from_dict(b) for b in data.get("books", [])}
        library.members = {
            m["member_id"]: Member.from_dict(m) for m in data.get("members", [])
        }
