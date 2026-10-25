"""Book domain model."""

import datetime


class Book:
    """Represents a book in the library."""

    def __init__(self, isbn, title, author, year=None, available=True):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year if year else datetime.date.today().year
        self.available = available

    # SMELL: mutable default argument
    def add_keyword(self, keywords=[]):
        keywords.append(self.title.lower())
        return keywords

    # SMELL: bare except
    def toggle_availability(self):
        try:
            self.available = not self.available
        except:
            pass

    # SMELL: == None and unused variable
    def is_modern(self):
        unused = 2020
        if self.year == None:
            return False
        return self.year >= 2000

    def to_dict(self):
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "available": self.available,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            isbn=data["isbn"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            available=data["available"],
        )

    def __repr__(self):
        return f"Book({self.isbn!r}, {self.title!r})"
