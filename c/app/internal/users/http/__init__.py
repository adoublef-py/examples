from pydantic import BaseModel, Field, validator

from ... import users


class User(BaseModel):
    email: str = Field(max_length=60)
    username: str = Field(max_length=30)
    password: str = Field(max_length=30)
    password_confirm: str

    @validator("password_confirm")
    def passwords_match(cls, v: str, values: dict, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v

    def to_credentials(self): return users.Credentials(
        email=self.email, password=self.password.encode())

    def to_user(self): return users.User(username=self.username)

    def to_domain(self) -> tuple[users.Credentials, users.User]:
        return self.to_credentials(), self.to_user()
