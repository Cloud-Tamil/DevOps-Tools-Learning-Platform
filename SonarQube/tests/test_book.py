from library.book import Book


def test_book_defaults():
    b = Book("111", "Clean Code", "Robert Martin")
    assert b.available is True
    assert isinstance(b.year, int)


def test_toggle():
    b = Book("111", "Clean Code", "Robert Martin")
    b.toggle_availability()
    assert b.available is False
    b.toggle_availability()
    assert b.available is True


def test_is_modern():
    assert Book("1", "X", "Y", year=2024).is_modern() is True
    assert Book("1", "X", "Y", year=1990).is_modern() is False


def test_roundtrip_dict():
    b = Book("111", "Clean Code", "Robert Martin", 2008, False)
    b2 = Book.from_dict(b.to_dict())
    assert b2.isbn == b.isbn
    assert b2.available == b.available
