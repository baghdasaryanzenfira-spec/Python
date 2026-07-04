#!/usr/bin/python3
from datetime import datetime, timedelta


class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed = {}
        self.history = []

    def borrow_book(self, book):
        if book.borrow():
            self.borrowed[book.isbn] = {
                "book": book,
                "due": datetime.now() + timedelta(days=14)
            }
            self.history.append(f"Borrowed {book.title}")
            return True
        return False

    def return_book(self, isbn):
        if isbn not in self.borrowed:
            return 0

        record = self.borrowed.pop(isbn)
        book = record["book"]
        due = record["due"]

        book.return_book()

        late_days = (datetime.now() - due).days
        fine = max(0, late_days)

        self.history.append(f"Returned {book.title} | Fine {fine}")
        return fine

    def __str__(self):
        return f"{self.name} ({self.member_id})"
