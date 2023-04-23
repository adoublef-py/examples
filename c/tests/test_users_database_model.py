from app.internal import users
from app.internal.users.database import Account, Profile


def test_domain_mapping_valid():
    user = users.User(username="test")
    creds = users.Credentials(email="test@mail.com",
                              password="password".encode())

    profile = Profile.from_user(user)
    assert profile.username == "test"
    assert profile.id == user.id

    account = Account.from_credentials(creds)
    assert account.created_at is not None