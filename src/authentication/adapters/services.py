from datetime import datetime, timedelta
from typing import Any, Dict

from passlib.context import CryptContext
import jwt

from src.config.envirenment import get_settings


_s = get_settings()


class Argon2HashService:
    _context = CryptContext(schemes=["argon2"], deprecated="auto")

    @staticmethod
    def hash_(value: str) -> str:
        return str(Argon2HashService._context.hash(value))

    @staticmethod
    def verify(value: str, hash_: str) -> bool:
        return bool(Argon2HashService._context.verify(value, hash_))


class JWTService:
    @staticmethod
    def _encode_token(*, data: Dict[str, Any], expire_minutes: int) -> str:
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
        return jwt.encode(
            {**data.copy(), "exp": expire}, _s.JWT_SECRET, algorithm=_s.JWT_ALGORITHM
        )

    @staticmethod
    def _decode_token(token: str) -> Dict[str, Any]:
        return jwt.decode(token, _s.JWT_SECRET, algorithms=[_s.JWT_ALGORITHM])
