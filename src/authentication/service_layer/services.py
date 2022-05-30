from src.authentication.domain.exceptions import EmailNotUniqueError, PasswordValidationError, UserNotFoundError
from src.authentication.domain.model import JWTService, Token, User, HashService
from src.authentication.domain.repository import UserRepository

from src.config.envirenment import get_settings
_s = get_settings()


def register_user(
    user: User,
    hash_service: HashService,
    repo: UserRepository
) -> User:
    existing_user = repo.get_by_email(user.email)
    if existing_user:
        raise EmailNotUniqueError(user.email)

    user.hash_password(hash_service)
    repo.add(user=user)

    return user


def login_user(
    email: str,
    password: str,
    hash_service: HashService,
    jwt_service: JWTService,
    repo: UserRepository
) -> Token:
    existing_user = repo.get_by_email(email)

    if not existing_user:
        raise UserNotFoundError()

    if not existing_user.password or not hash_service.verify(password, existing_user.password):
        raise PasswordValidationError()

    return Token(
        access_token=jwt_service._encode_token(
            data={'id': existing_user.id, 'email': existing_user.email}, expire_minutes=_s.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        refresh_token=jwt_service._encode_token(
            data={}, expire_minutes=_s.JWT_REFRESH_TOKEN_EXPIRE_MINUTES),
    )
