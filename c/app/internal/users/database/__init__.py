from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field, Session, select

from ... import users


class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    email: str = Field()
    password: bytes = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def from_credentials(cls, credentials: users.Credentials) -> "Account":
        return cls(email=credentials.email, password=credentials.password)

    def to_credentials(self) -> users.Credentials:
        return users.Credentials(email=self.email, password=self.password)


class Profile(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    username: str = Field()
    bio: str | None = Field(default=None)
    photo_url: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def from_user(cls, user: users.User) -> "Profile":
        """NOTE can this be converted to use a `cls(**user.dict())`"""
        return cls(id=user.id, username=user.username, bio=user.bio, photo_url=user.photo_url)

    def to_user(self) -> users.User:
        return users.User(id=self.id, username=self.username, bio=self.bio, photo_url=self.photo_url)


class UserRepository(ABC):
    @abstractmethod
    def insert_user(self, user: users.User, credentials: users.Credentials) -> users.User:
        pass

    @abstractmethod
    def fetch_user_list(self) -> list[users.User]:
        pass

    @abstractmethod
    def find_user_by_id(self, id: UUID) -> users.User:
        pass


class PostgresRepository(UserRepository):
    db: Session

    def __init__(self, db: Session):
        self.db = db

    def insert_user(self, user: users.User, credentials: users.Credentials) -> users.User:
        account = Account.from_credentials(credentials)
        profile = Profile.from_user(user)

        self.db.add(account)
        self.db.add(profile)

        self.db.commit()

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
