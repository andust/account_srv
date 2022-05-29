
from typing import Optional, Protocol

from src.authentication.domain.exceptions import PasswordValidationError


class HashService(Protocol):
    @staticmethod
    def hash_(value: str) -> str:
        ...

    @staticmethod
    def verify(value: str, hash_: str) -> bool:
        ...


class User:
    def __init__(self, full_name: str, email: str, password: Optional[str] = None):
        self.id = None
        self.full_name = full_name
        self.email = email
        self.password = password

    def hash_password(self, hash_service: HashService) -> None:
        if not self.password:
            raise PasswordValidationError()

        self.password = hash_service.hash_(self.password)
