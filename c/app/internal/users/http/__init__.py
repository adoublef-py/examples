from datetime import timedelta
from fastapi import APIRouter
from pydantic import BaseModel, Field, validator

from ... import users


router = APIRouter()


class Register(BaseModel):
    email: str = Field(max_length=60)
    username: str = Field(max_length=30)
    password: str = Field(max_length=30)
    password_confirm: str  # this may not exist in the response body

    @validator("password_confirm")
    def passwords_match(cls, v: str, values: dict, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v

    def to_credentials(self):
        return users.parse_credentials(email=self.email, password=self.password)

    def to_user(self): return users.User(username=self.username)

    def to_domain(self) -> tuple[users.Credentials, users.User]:
        return self.to_credentials(), self.to_user()


@router.post("/", status_code=201)
async def handle_register(register: Register):
    return {"message": "user created successfully"}


class Credentials(BaseModel):
    email: str = Field(max_length=60)
    password: str = Field(max_length=30)

    def to_credentials(self) -> users.Credentials:
        return users.parse_credentials(email=self.email, password=self.password)


@router.post("/auth")
async def handle_login(credentials: Credentials):
    return {"message": "user logged in successfully"}


@router.delete("/auth", status_code=204)
async def handle_logout():
    return
