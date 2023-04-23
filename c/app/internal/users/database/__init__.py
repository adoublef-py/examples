from datetime import datetime
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field

from ... import users


class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    email: str = Field()
    password: bytes = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def from_credentials(self, credentials: users.Credentials):
        pass

    def to_credentials(self) -> users.Credentials:
        pass


class Profile(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    username: str = Field()
    bio: str | None = Field(default=None)
    photo_url: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def from_user(self, user: users.User):
        pass

    def to_user(self) -> users.User:
        pass
