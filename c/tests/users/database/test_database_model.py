from app.internal import users
from app.internal.users import database as db


def test_domain_mapping_valid():
    user = users.User(username="test")
    creds = users.Credentials(email="test@mail.com",
                              password="password".encode())

    # check that credentials are valid
    creds.compare_password("password")

    pass
