#!/usr/bin/python3
from datetime import datetime

class Book:
    def __init__(self,title,author,isbn,copies=1):
        self.title=title
        self.author=author
        self.isbn=isbn
        self.copies=copies
        self.available=copies
    def borrow(self):
        if self.available<=0:
            return False
        self.available-=1
        return True
    def return_book(self):
        if self.available<self.copies:
            self.available+=1
    def __str__(self):
        return f"{self.title} | {self.author} | {self.isbn} | {self.available}/{self.copies}"
