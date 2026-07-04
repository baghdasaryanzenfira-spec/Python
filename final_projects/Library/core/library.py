#!/usr/bin/python3
from datetime import datetime
from models.book import Book
import os
import json
from models.member import Member


class Library:

    def __init__(self,filename="library_data.json"):
        self.filename=filename
        self.books = []
        self.members = []
        self.load_data()

    def add_book(self, book):
        self.books.append(book)
        self.save_data()

    def add_member(self, member):
        self.members.append(member)
        self.save_data()

    def show_members(self):
        for m in self.members:
            print(m)


    def save_data(self):
        books_data=[]
        for book in self.books:
            books_data.append({
                "title":book.title,
                "author":book.author,
                "isbn":book.isbn,
                "copies":book.copies,
                "available":book.available
                })
        members_data=[]
        for member in self.members:
            members_data.append({
                "member_id":member.member_id,
                "name":member.name,
                "borrowed":{
                    isbn: rec["due"].isoformat()
                    for isbn, rec in member.borrowed.items()
                    },
                "history":member.history
                })
        all_data={
                "books":books_data,
                "members":members_data
                }
        with open(self.filename,"w",encoding="utf-8") as f:
            json.dump(all_data,f,indent=4,ensure_ascii=False)

    def load_data(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename,"r",encoding="utf-8") as f:
            try:
                all_data=json.load(f)
            except json.JSONDecodeError:
                return
        if not isinstance(all_data, dict):
            return
        for i in all_data.get("books",[]):
            book=Book(i["title"],i["author"],i["isbn"],i["copies"])
            book.available=i["available"]
            self.books.append(book)
        book_map={b.isbn: b for b in self.books}
        for i in all_data.get("members",[]):
            member=Member(i["name"],i["member_id"])
            for isbn, due_str in i.get("borrowed",{}).items():
                book=book_map.get(isbn)
                if book:
                    member.borrowed[isbn]={
                        "book":book,
                        "due":datetime.fromisoformat(due_str)
                        }
            member.history=i.get("history",[])
            self.members.append(member)

    def show_books(self):
        for b in self.books:
            print(b)


    def search(self, keyword):
        return [
            b for b in self.books
            if keyword.lower() in b.title.lower()
            or keyword.lower() in b.author.lower()
        ]

    def borrow(self, member_id, isbn):
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.isbn == isbn), None)

        if not member or not book:
            return "Not found"

        if member.borrow_book(book):
            self.save_data()
            return "Success"
        return "Unavailable"

    # -------- return --------
    def return_book(self, member_id, isbn):
        member = next((m for m in self.members if m.member_id == member_id), None)

        if not member:
            return "No member"

        fine = member.return_book(isbn)
        self.save_data()
        return f"Returned | Fine: {fine}"

    # -------- stats --------
    def stats(self):
        return {
            "books": len(self.books),
            "members": len(self.members)
        }
