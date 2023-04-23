from pytest import fixture, FixtureRequest
from testcontainers.postgres import PostgresContainer
from uuid import UUID
from sqlmodel import SQLModel, Session, create_engine, select

from app.internal.users.database import Account, Profile
from app.internal import users


@fixture(scope="session")
def session():
    with PostgresContainer() as postgres:
        engine = create_engine(postgres.get_connection_url())

        SQLModel.metadata.create_all(engine)

        with Session(engine) as session:
            yield session


def test_insert_author(session: Session):
    user = users.User(username="test")
    credentials = users.Credentials(
        email="test@mail.com", password=b"password")

    insert_user(session, user, credentials)


def test_get_user_list(session: Session):
    # retrieve the user_list
    user_list = get_user_list(session)
    assert len(user_list) == 1

    # get the user by id
    found = find_user_by_id(session, user_list[0].id)
    assert found.username == "test"


def insert_user(db: Session, user: users.User, credentials: users.Credentials) -> users.User:
    """
    Insert a new user into the database.
    """
    account = Account.from_credentials(credentials)
    profile = Profile.from_user(user)

    db.add(account)
    db.add(profile)
    db.commit()

    return user


def get_user_list(db: Session):
    """
    Get a list of all users.
    """
    statement = select(Profile)
    profiles = db.exec(statement).fetchall()

    for profile in profiles:
        print(profile)

    return [profile.to_user() for profile in profiles]


def find_user_by_id(db: Session, id: UUID) -> users.User:
    """
    Find a user by their email address.
    """
    statement = select(Profile).where(Profile.id == id)
    profile = db.exec(statement).first()
    return profile.to_user()
