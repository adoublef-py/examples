from pytest import raises
from pydantic import ValidationError

from app.internal.users import http


def test_user_invalid():
    user_input = {
        "email": "test@mail.com",
        "password": "password",
    }

    with raises(ValidationError):
        http.User(**user_input)


def test_user_valid():
    user_input = {
        "email": "test@mail.com",
        "username": "test",
        "password": "password",
        "password_confirm": "password",
    }

    user = http.User(**user_input)
    assert user.email == "test@mail.com"


def test_domain_mapping_valid():
    user_input = {
        "email": "test@mail.com",
        "username": "test",
        "password": "password",
        "password_confirm": "password",
    }

    user = http.User(**user_input)
    credentials, author = user.to_domain()

    # invalid password should throw an error
    with raises(ValueError):
        credentials.compare_password("not the password")

    # valid password should not throw an error
    credentials.compare_password("password")

    assert author.username == "test"
    assert author.id is not None
