from datetime import datetime, timedelta
from uuid import UUID, uuid4
from bcrypt import hashpw, gensalt, checkpw
from dataclasses import dataclass, field
from jose import JWTError, jwt


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


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create an access token that expires in `expires_delta` minutes.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
