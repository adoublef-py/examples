from uuid import UUID, uuid4
from bcrypt import hashpw, gensalt, checkpw
from dataclasses import dataclass, field


@dataclass
class Credentials:
    email: str
    password: bytes

    def compare_password(self, password: str):
        if not checkpw(password.encode(), self.password):
            raise ValueError("passwords do not match")

    @classmethod
    def parse(cls, email: str, password: str) -> "Credentials":
        """
        Parse a user's email and password into a `Credentials` object.
        It will validate the email and hash the password.
        """
        hash = hashpw(password=password.encode(), salt=gensalt())
        return cls(email=email, password=hash)


@dataclass
class User:
    username: str
    # default arguments must follow non-default arguments
    id: UUID = field(default_factory=uuid4)
    bio: str | None = None
    photo_url: str | None = None


def parse_credentials(email: str, password: str) -> Credentials:
    """
    Parse a user's email and password into a `Credentials` object.
    It will validate the email and hash the password.
    """
    hash = hashpw(password=password.encode(), salt=gensalt())
    return Credentials(email=email, password=hash)
