
from typing import Any, Dict, Optional, Protocol
from dataclasses import dataclass
from enum import Enum

from src.authentication.domain.exceptions import PasswordValidationError


class TokenType(str, Enum):
    bearer = "bearer"


@dataclass
class Token:
    access_token: str
    refresh_token: str
    token_type: TokenType = TokenType.bearer


class HashService(Protocol):
    @staticmethod
    def hash_(value: str) -> str:
        ...

    @staticmethod
    def verify(value: str, hash_: str) -> bool:
        ...


class JWTService(Protocol):
    @staticmethod
    def _encode_token(*, data: Dict[str, Any], expire_minutes: int) -> str:
        ...

    @staticmethod
    def _decode_token(token: str) -> Dict[str, Any]:
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
