from abc import ABC, abstractmethod
from typing import Callable, Type
from uuid import UUID, uuid4
from pytest import fixture, raises, mark
from pydantic import BaseModel, Field, ValidationError, confloat, constr

# core/books/models.py


class Book(BaseModel):  # this is the domain model
    id: UUID | None = uuid4()
    title: str
    author: constr(min_length=1, regex="[A-Za-z ,.'-]+$")
    price: confloat(gt=0)
    year: int | None = None

# core/books/database/models.py


class BookDB(Book):  # this is the model that will be stored in the database
    id: UUID = Field(default_factory=uuid4())


# core/books/database/repository.py
class BookRepository(ABC):
    @abstractmethod
    def insert_book(self, book: Book) -> UUID:
        raise NotImplementedError

    @abstractmethod
    def get_book_by_id(self, id: UUID) -> Book:
        raise NotImplementedError

    @abstractmethod
    def get_book_list(self) -> list[Book]:
        raise NotImplementedError


class InMemRepository(BookRepository):
    books: dict[UUID, BookDB] = dict()

    def insert_book(self, book: Book) -> UUID:
        if not isinstance(book, Book):
            raise TypeError(f"book must be of type {Book}")

        # convert the domain-level book to a database-level book
        book_db = BookDB(**book.dict())

        # save the book to the database
        self.books[book_db.id] = book_db

        return book_db.id

    def get_book_by_id(self, id: UUID) -> Book:
        pass

    def get_book_list(self) -> list[Book]:
        """get the books from the database and return a list of domain-level book objects"""
        return [Book(**book.dict()) for book in self.books.values()]

# test/test_books_schema.py


@fixture()
def book_repository() -> BookRepository:
    return InMemRepository()


@fixture()
def book_input() -> Book:
    return Book(title="This is a nice book",
                author="Jane Appleseed", price=18.99, year=1856)


def test_insert_book(book_repository: BookRepository, book_input: Book):
    # add the book to the database
    _ = book_repository.insert_book(book_input)

    # get list of books from the database
    books = book_repository.get_book_list()

    assert len(books) == 1
    assert books[0].title == book_input.title
    assert books[0].author == book_input.author
    assert books[0].price == book_input.price
    assert books[0].year == book_input.year


def test_invalid_book(book_repository: BookRepository):
    with raises(TypeError):
        book_input = dict(title="This is a nice book")
        _ = book_repository.insert_book(book_input)


@mark.parametrize("schema", [
    dict(title="This is a nice book",
         author="Jane Appleseed", price=18.99, year=1856),
    dict(title="This is another nice book", author="John Smith", price=18.99)
])
def test_create_book_ok(schema: dict):
    book = Book(
        title=schema.get("title"),
        author=schema.get("author"),
        price=schema.get("price"),
        year=schema.get("year"),
    )
    assert book.title == schema.get("title")
    assert book.author == schema.get("author")
    assert book.price == schema.get("price")
    assert book.year == schema.get("year")


@mark.parametrize("schema", [
    dict(title="This is a nice book",
         author="Jane Appleseed", year=1856),
    dict(title="This is another nice book", price=18.99)
])
def test_create_book_not_ok(schema: dict):
    with raises(ValidationError):
        Book(
            title=schema.get("title"),
            author=schema.get("author"),
            price=schema.get("price"),
            year=schema.get("year"),
        )
