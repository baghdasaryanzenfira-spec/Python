#!/usr/bin/python3
import json


def save_data(library, filename="library_data.json"):
    data = {
        "books": [
            {
                "title": b.title,
                "author": b.author,
                "isbn": b.isbn,
                "copies": b.copies,
                "available": b.available,
            }
            for b in library.books
        ],
        "members": [
            {
                "name": m.name,
                "member_id": m.member_id,
                "borrowed": {isbn: rec["due"].isoformat() for isbn, rec in m.borrowed.items()},
                "history": m.history,
            }
            for m in library.members
        ],
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_data(filename="library_data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
