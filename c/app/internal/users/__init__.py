from uuid import UUID, uuid4
from bcrypt import hashpw, gensalt, checkpw
from dataclasses import dataclass, field


@dataclass
class Credentials:
    email: str
    password: bytes

    def __post_init__(self):
        """
        The password needs to be stored as a hash, not in plain text.
        Therefore we use the `__post_init__` hook to hash the password.
        """
        self.password = hashpw(self.password, gensalt())

    def compare_password(self, password: str):
        if not checkpw(password.encode(), self.password):
            raise ValueError("passwords do not match")


@dataclass
class User:
    username: str
    # default arguments must follow non-default arguments
    id: UUID = field(default_factory=uuid4)
    bio: str | None = None
    photo_url: str | None = None
