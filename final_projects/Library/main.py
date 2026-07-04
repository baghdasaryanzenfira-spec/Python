#!/usr/bin/python3
from core.library import Library
from models.book import Book
from models.member import Member


def main():
    lib = Library()

    while True:
        print("\n===== LIBRARY =====")
        print("1 Add book")
        print("2 Show books")
        print("3 Add member")
        print("4 Show members")
        print("5 Borrow")
        print("6 Return")
        print("7 Search")
        print("8 Stats")
        print("0 Exit")

        choice = input(">> ")

        if choice == "1":
            lib.add_book(Book(
                input("Title: "),
                input("Author: "),
                input("ISBN: "),
                int(input("Copies: "))
            ))

        elif choice == "2":
            lib.show_books()

        elif choice == "3":
            lib.add_member(Member(
                input("Name: "),
                input("ID: ")
            ))

        elif choice == "4":
            lib.show_members()

        elif choice == "5":
            print(lib.borrow(
                input("Member ID: "),
                input("ISBN: ")
            ))

        elif choice == "6":
            print(lib.return_book(
                input("Member ID: "),
                input("ISBN: ")
            ))

        elif choice == "7":
            for b in lib.search(input("Keyword: ")):
                print(b)

        elif choice == "8":
            print(lib.stats())

        elif choice == "0":
            break


if __name__ =="__main__":
    main()
