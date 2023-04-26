from abc import ABC, abstractmethod
from typing import Callable, Type
from uuid import UUID, uuid4
from pytest import fixture, raises, mark
from pydantic import BaseModel, Field, ValidationError, confloat, constr

from core.books.database.repository import InMemRepository
from core.books import book


def test_insert_book():
    book_input = book.Book(title="This is a nice book",
                           author="Jane Appleseed", price=18.99, year=1856)

    book_repository = InMemRepository()
    # add the book to the database
    _ = book_repository.insert_book(book_input)

    # get list of books from the database
    books = book_repository.get_book_list()

    assert len(books) == 1
    assert books[0].title == book_input.title
    assert books[0].author == book_input.author
    assert books[0].price == book_input.price
    assert books[0].year == book_input.year


def test_invalid_book():
    book_repository = InMemRepository()

    with raises(TypeError):
        book_input = dict(title="This is a nice book")
        _ = book_repository.insert_book(book_input)

    books = book_repository.get_book_list()

    assert len(books) == 0


@mark.parametrize("schema", [
    dict(title="This is a nice book",
         author="Jane Appleseed", price=18.99, year=1856),
    dict(title="This is another nice book", author="John Smith", price=18.99)
])
def test_create_book_ok(schema: dict):
    book_input = book.Book(
        title=schema.get("title"),
        author=schema.get("author"),
        price=schema.get("price"),
        year=schema.get("year"),
    )
    assert book_input.title == schema.get("title")
    assert book_input.author == schema.get("author")
    assert book_input.price == schema.get("price")
    assert book_input.year == schema.get("year")


@mark.parametrize("schema", [
    dict(title="This is a nice book",
         author="Jane Appleseed", year=1856),
    dict(title="This is another nice book", price=18.99)
])
def test_create_book_not_ok(schema: dict):
    with raises(ValidationError):
        book.Book(
            title=schema.get("title"),
            author=schema.get("author"),
            price=schema.get("price"),
            year=schema.get("year"),
        )
