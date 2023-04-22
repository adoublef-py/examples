import pydantic
from pytest import raises, mark
from pydantic import BaseModel, confloat, constr


class Book(BaseModel):
    title: str
    author: constr(min_length=1, regex="[A-Za-z ,.'-]+$")
    price: confloat(gt=0)
    year: int | None = None


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
    with raises(pydantic.ValidationError):
        Book(
            title=schema.get("title"),
            author=schema.get("author"),
            price=schema.get("price"),
            year=schema.get("year"),
        )
