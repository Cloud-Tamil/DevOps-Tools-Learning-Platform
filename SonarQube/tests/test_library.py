import pytest

from library.book import Book
from library.library import Library
from library.member import Member


@pytest.fixture
def lib():
    return Library()


def test_add_and_find(lib):
    lib.add_book(Book("111", "A", "X"))
    assert lib.find_book("111").title == "A"


def test_borrow_success(lib):
    lib.add_book(Book("111", "A", "X"))
    lib.register_member(Member("m1", "Alice"))
    lib.borrow_book("m1", "111")
    assert lib.books["111"].available is False
    assert lib.members["m1"].borrowed == ["111"]


def test_borrow_unavailable(lib):
    b = Book("111", "A", "X", available=False)
    lib.add_book(b)
    lib.register_member(Member("m1", "Alice"))
    with pytest.raises(ValueError):
        lib.borrow_book("m1", "111")


def test_availability_rate_empty(lib):
    # Currently raises ZeroDivisionError → will be caught by Sonar as a bug
    with pytest.raises(ZeroDivisionError):
        lib.availability_rate()


def test_report(lib):
    lib.add_book(Book("111", "A", "X"))
    lib.add_book(Book("222", "B", "Y", available=False))
    lib.register_member(Member("m1", "Alice"))
    r = lib.monthly_report()
    assert r["total_books"] == 2
    assert r["available"] == 1
    assert r["borrowed"] == 1
