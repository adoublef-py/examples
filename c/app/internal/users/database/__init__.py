from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID
from sqlmodel import Relationship, SQLModel, Field, Session, select

from ... import users


class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    email: str = Field(unique=True)
    password: bytes = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # https://stackoverflow.com/questions/70759112/one-to-one-relationships-with-sqlmodel
    profile: Optional["Profile"] = Relationship(back_populates="account",
                                                sa_relationship_kwargs={"uselist": False})

    @classmethod
    def from_credentials(cls, credentials: users.Credentials) -> "Account":
        return cls(email=credentials.email, password=credentials.password)

    def to_credentials(self) -> users.Credentials:
        return users.Credentials(email=self.email, password=self.password)


class Profile(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    username: str = Field(unique=True)
    bio: str | None = Field(default=None)
    photo_url: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    account_id: int | None = Field(
        default=None, foreign_key="account.id", nullable=False)
    account: Optional["Account"] = Relationship(back_populates="profile")

    @classmethod
    def from_user(cls, user: users.User) -> "Profile":
        """NOTE can this be converted to use a `cls(**user.dict())`"""
        return cls(id=user.id, username=user.username, bio=user.bio, photo_url=user.photo_url)

    def to_user(self) -> users.User:
        return users.User(id=self.id, username=self.username, bio=self.bio, photo_url=self.photo_url)


class UserRepository(ABC):
    @abstractmethod
    def insert_user(self, user: users.User, credentials: users.Credentials) -> users.User:
        """
        Insert a new user into the database.
        """
        pass

    @abstractmethod
    def fetch_user_list(self) -> list[users.User]:
        """
        Fetch a list of all users.
        """
        pass

    @abstractmethod
    def find_user_by_id(self, id: UUID) -> users.User:
        """
        Find a user by their id.
        """
        pass

    @abstractmethod
    def find_user_by_credentials(self, email: str, password: str) -> users.User:
        """
        Find a user by their email.
        """
        pass


class PostgresRepository(UserRepository):
    db: Session

    def __init__(self, db: Session):
        self.db = db

    def insert_user(self, user: users.User, credentials: users.Credentials) -> users.User:
        account = Account(
            email=credentials.email,
            password=credentials.password,
        )

        try:
            self.db.add(account)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

        profile = Profile(
            id=user.id,
            username=user.username,
            bio=user.bio,
            photo_url=user.photo_url,
            account=account,
        )

        try:
            self.db.add(profile)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

        return user

    def fetch_user_list(self):
        statement = select(Profile)
        profiles = self.db.exec(statement).fetchall()

        # for profile in profiles: yield profile.to_user()
        return [profile.to_user() for profile in profiles]

    def find_user_by_id(self, id: UUID) -> users.User:
        statement = select(Profile).where(Profile.id == id)
        profile = self.db.exec(statement).first()

        return profile.to_user()

    def find_user_by_credentials(self, email: str, password: str) -> users.User:
        statement = select(Account).where(Account.email == email)
        account = self.db.exec(statement).first()

        if account is None:
            raise Exception("User not found")

        # NOTE: possible exception caused here
        credentials = users.Credentials(
            email=account.email, password=account.password)

        credentials.compare_password(password)

        statement = select(Profile).where(Profile.account_id == account.id)
        profile = self.db.exec(statement).first()

        return profile.to_user()
