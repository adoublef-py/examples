from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field

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
        return users.User(
            id=self.id,
            username=self.username,
            bio=self.bio,
            photo_url=self.photo_url,
        )


class UserRepository(ABC):
    @abstractmethod
    def insert_user(self, user: users.User, credentials: users.Credentials) -> users.User:
        pass


class InMemRepository(UserRepository):
    pass
