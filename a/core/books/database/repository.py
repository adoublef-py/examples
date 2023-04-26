from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from pydantic import Field
from core.books import book


class Book(book.Book):  # this is the model that will be stored in the database
    id: UUID = Field(default_factory=uuid4)


# core/books/database/repository.py
class BookRepository(ABC):
    @abstractmethod
    def insert_book(self, book_input: book.Book) -> UUID:
        raise NotImplementedError

    @abstractmethod
    def get_book_by_id(self, id: UUID) -> book.Book:
        raise NotImplementedError

    @abstractmethod
    def get_book_list(self) -> list[book.Book]:
        raise NotImplementedError


class InMemRepository(BookRepository):
    books: dict[UUID, Book]

    def __init__(self):
        self.books = dict()

    def insert_book(self, book_input: book.Book) -> UUID:
        if not isinstance(book_input, book.Book):
            raise TypeError(f"book must be of type {book.Book}")

        # convert the domain-level book to a database-level book
        book_db = Book(**book_input.dict())

        # save the book to the database
        self.books[book_db.id] = book_db

        return book_db.id

    def get_book_by_id(self, id: UUID) -> book.Book:
        pass

    def get_book_list(self) -> list[book.Book]:
        """get the books from the database and return a list of domain-level book objects"""
        return [book.Book(**book_input.dict()) for book_input in self.books.values()]
