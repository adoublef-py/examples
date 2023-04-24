from pytest import fixture, raises
from testcontainers.postgres import PostgresContainer
from sqlmodel import SQLModel, Session, create_engine

from app.internal.users.database import PostgresRepository, UserRepository
from app.internal.users import User, parse_credentials


# https://docs.pytest.org/en/6.2.x/fixture.html
# https://betterprogramming.pub/understand-5-scopes-of-pytest-fixtures-1b607b5c19ed
@fixture(scope="session")
def user_repo():
    with PostgresContainer() as postgres:
        engine = create_engine(postgres.get_connection_url())

        SQLModel.metadata.create_all(engine)

        with Session(engine) as session:
            yield PostgresRepository(session)


def test_insert_author_valid(user_repo: UserRepository):
    user = User(username="test")
    credentials = parse_credentials(
        email="test@mail.com", password="password")

    user_repo.insert_user(user, credentials)


def test_insert_author_duplicate_username(user_repo: UserRepository):
    user = User(username="test")
    credentials = parse_credentials(
        email="test-1@mail.com", password="password")

    with raises(Exception):
        user_repo.insert_user(user, credentials)

def test_insert_author_duplicate_email(user_repo: UserRepository):
    user = User(username="test-1")
    credentials = parse_credentials(
        email="test@mail.com", password="password")

    with raises(Exception):
        user_repo.insert_user(user, credentials)


def test_get_user_list_valid(user_repo: UserRepository):
    # retrieve the user_list
    user_list = user_repo.fetch_user_list()
    assert len(user_list) == 1

    # get the user by id
    found = user_repo.find_user_by_id(user_list[0].id)
    assert found.username == "test"


def test_get_user_by_credentials_valid(user_repo: UserRepository):
    # get the user by credentials
    user_repo.find_user_by_credentials(
        email="test@mail.com", password="password")
