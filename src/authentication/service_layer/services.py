from src.authentication.domain.exceptions import EmailNotUniqueError
from src.authentication.domain.model import User, HashService
from src.authentication.domain.repository import UserRepository


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
