import os
import tempfile

from library.book import Book
from library.library import Library
from library.storage import Storage


def test_save_and_load_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "lib.json")
        lib = Library(Storage(path))
        lib.add_book(Book("111", "A", "X"))
        lib2 = Library(Storage(path)).load()
        assert "111" in lib2.books


def test_load_missing_file_is_noop():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "missing.json")
        lib = Library(Storage(path)).load()
        assert lib.books == {}
