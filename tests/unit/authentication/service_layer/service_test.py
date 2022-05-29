import pytest
from src.authentication.adapters.services import Argon2HashService
from src.authentication.domain.model import User
from src.authentication.domain.exceptions import EmailNotUniqueError
from src.authentication.domain.repository import FakeRepository

from src.authentication.service_layer import services

hash_service = Argon2HashService()


def _get_user(name: str = "Andrzej", email: str = "andrzej@example.com", password: str = "password"):
    return User(name, email, password)


@pytest.mark.unit
def test_hash_service_hash_string():
    string_to_hash = "password"
    hashed_string = hash_service.hash_(string_to_hash)

    assert string_to_hash != hashed_string


@pytest.mark.unit
def test_raise_email_not_unique_exception_if_try_to_register_same_user():
    new_user = _get_user()
    repository = FakeRepository([])
    repository.add(new_user)

    with pytest.raises(EmailNotUniqueError):
        services.register_user(user=new_user,
                               hash_service=hash_service,
                               repo=repository)


@pytest.mark.unit
def test_registered_user_password_is_hashed():
    new_user_password = "password"
    new_user = _get_user(password=new_user_password)
    repository = FakeRepository([])

    services.register_user(user=new_user,
                           hash_service=hash_service,
                           repo=repository)

    assert len(new_user.password) > len(new_user_password)
    assert new_user.password != new_user_password


@pytest.mark.unit
def test_user_is_saved_to_db():
    new_user = _get_user()
    repository = FakeRepository([])

    services.register_user(user=new_user,
                           hash_service=hash_service,
                           repo=repository)

    saved_user = repository.get_by_email(new_user.email)

    assert saved_user is not None
