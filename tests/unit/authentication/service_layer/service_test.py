import pytest

from src.authentication.adapters.services import Argon2HashService, JWTService
from src.authentication.domain.model import User
from src.authentication.domain.exceptions import EmailNotUniqueError
from src.authentication.domain.repository import FakeRepository
from src.authentication.service_layer import services
from src.config.envirenment import get_settings


_s = get_settings()


def _get_user(name: str = "Andrzej", email: str = "andrzej@example.com", password: str = "password"):
    return User(name, email, password)


@pytest.mark.unit
def test_hash_service_hash_string():
    string_to_hash = "password"
    hashed_string = Argon2HashService.hash_(string_to_hash)

    assert string_to_hash != hashed_string


@pytest.mark.unit
def test_raise_email_not_unique_exception_if_try_to_register_same_user():
    new_user = _get_user()
    repository = FakeRepository([])
    repository.add(new_user)

    with pytest.raises(EmailNotUniqueError):
        services.register_user(user=new_user,
                               hash_service=Argon2HashService,
                               repo=repository)


@pytest.mark.unit
def test_registered_user_password_is_hashed():
    new_user_password = "password"
    new_user = _get_user(password=new_user_password)
    repository = FakeRepository([])

    services.register_user(user=new_user,
                           hash_service=Argon2HashService,
                           repo=repository)

    assert len(new_user.password or "") > len(new_user_password)
    assert new_user.password != new_user_password


@pytest.mark.unit
def test_user_is_saved_to_db():
    new_user = _get_user()
    repository = FakeRepository([])

    services.register_user(user=new_user,
                           hash_service=Argon2HashService,
                           repo=repository)

    saved_user = repository.get_by_email(new_user.email)

    assert saved_user is not None


@pytest.mark.unit
def test_jwt_service_encode_token():
    token = JWTService._encode_token(
        data={"user_id": 1}, expire_minutes=_s.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    assert isinstance(token, str)
    assert len(token) > 100


@pytest.mark.unit
def test_jwt_service_decode_token():
    payload = {"user_id": 1}
    token = JWTService._encode_token(
        data=payload, expire_minutes=_s.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    decoded_jwt = JWTService._decode_token(token)

    assert decoded_jwt["user_id"] is payload["user_id"]
    assert decoded_jwt['exp']


@pytest.mark.unit
def test_successful_user_login():
    user_raw_password = "secret password"
    new_user = _get_user(password=user_raw_password)
    repository = FakeRepository([])

    services.register_user(user=new_user,
                           hash_service=Argon2HashService,
                           repo=repository)

    token = services.login_user(email=new_user.email,
                                password=user_raw_password,
                                hash_service=Argon2HashService,
                                jwt_service=JWTService,
                                repo=repository)

    assert token.access_token is not None
    assert token.refresh_token is not None
    assert token.token_type == 'bearer'
