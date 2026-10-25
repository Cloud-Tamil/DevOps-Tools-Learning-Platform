"""Core library service."""

from library.book import Book
from library.member import Member


class Library:
    """In-memory library service with persistence hooks."""

    def __init__(self, storage=None):
        self.books = {}
        self.members = {}
        self.storage = storage

    # ---------- Book management ----------

    def add_book(self, book):
        # BUG: no duplicate ISBN check
        self.books[book.isbn] = book
        self._persist()

    def remove_book(self, isbn):
        # BUG: raises KeyError silently if missing
        del self.books[isbn]
        self._persist()

    def find_book(self, isbn):
        return self.books.get(isbn)

    def search_books(self, query):
        # SMELL: does 3 passes; could be one comprehension
        result = []
        for b in self.books.values():
            if query.lower() in b.title.lower():
                result.append(b)
        return result

    # ---------- Member management ----------

    def register_member(self, member):
        self.members[member.member_id] = member
        self._persist()

    def borrow_book(self, member_id, isbn):
        member = self.members.get(member_id)
        book = self.books.get(isbn)

        # BUG: no None checks
        if not book.available:
            raise ValueError("Book not available")
        if not member.can_borrow():
            raise ValueError("Borrow limit reached")

        book.toggle_availability()
        member.borrow(isbn)
        self._persist()

    def return_book(self, member_id, isbn):
        member = self.members.get(member_id)
        book = self.books.get(isbn)

        # BUG: no validation that the member actually has the book
        member.return_book(isbn)
        book.toggle_availability()
        self._persist()

    # ---------- Reporting ----------

    # BUG: division by zero when no books
    def availability_rate(self):
        available = [b for b in self.books.values() if b.available]
        return len(available) / len(self.books)

    # SMELL: method too long, duplicated error handling
    def monthly_report(self):
        total = len(self.books)
        avail = len([b for b in self.books.values() if b.available])
        borrowed = total - avail
        members = len(self.members)
        active = len([m for m in self.members.values() if m.borrowed])

        if total > 0:
            rate = avail / total
        else:
            rate = 0

        report = {
            "total_books": total,
            "available": avail,
            "borrowed": borrowed,
            "members": members,
            "active_members": active,
            "availability_rate": rate,
        }
        return report

    # ---------- Persistence ----------

    def _persist(self):
        if self.storage:
            self.storage.save(self)

    def load(self):
        if self.storage:
            self.storage.load(self)
        return self
