"""Member domain model."""

import datetime


class Member:
    """A registered library member."""

    MAX_BORROW = 5

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed = []
        self.joined = datetime.date.today()

    def borrow(self, isbn):
        # BUG: no duplicate check, no max check
        self.borrowed.append(isbn)

    def return_book(self, isbn):
        # BUG: no membership check → ValueError on missing isbn
        self.borrowed.remove(isbn)

    # SMELL: overly complex boolean expression (simplifiable)
    def can_borrow(self):
        if len(self.borrowed) < self.MAX_BORROW:
            return True
        else:
            return False

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "borrowed": list(self.borrowed),
            "joined": self.joined.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        m = cls(data["member_id"], data["name"])
        m.borrowed = list(data["borrowed"])
        m.joined = datetime.date.fromisoformat(data["joined"])
        return m

    def __repr__(self):
        return f"Member({self.member_id!r}, {self.name!r})"
