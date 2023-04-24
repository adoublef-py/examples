from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture
from app.internal.users.http import router as users_router, Register, Credentials


app = FastAPI()

app.include_router(users_router)

client = TestClient(app)


def test_register_user():
    user_input = {
        "email": "test@mail.com",
        "username": "test",
        "password": "password",
        "password_confirm": "password",
    }

    response = client.post("/", json=user_input)
    assert response.status_code == 201


def test_login_user():
    credentials_input = {
        "email": "test@mail.com",
        "password": "password",
    }

    response = client.post("/auth", json=credentials_input)
    assert response.status_code == 200

    # check that the response contains a token
    # check that a cookie was set
