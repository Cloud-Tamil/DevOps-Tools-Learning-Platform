from library.member import Member


def test_borrow_limit():
    m = Member("m1", "Alice")
    for i in range(5):
        m.borrow(f"isbn{i}")
    assert m.can_borrow() is False


def test_return():
    m = Member("m1", "Alice")
    m.borrow("isbn1")
    m.return_book("isbn1")
    assert m.borrowed == []


def test_roundtrip_dict():
    m = Member("m1", "Alice")
    m.borrow("isbn1")
    m2 = Member.from_dict(m.to_dict())
    assert m2.member_id == "m1"
    assert m2.borrowed == ["isbn1"]
