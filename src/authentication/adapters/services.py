from passlib.context import CryptContext


class Argon2HashService:
    def __init__(self) -> None:
        self._context = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash_(self, value: str) -> str:
        return str(self._context.hash(value))

    def verify(self, value: str, hash_: str) -> bool:
        return bool(self._context.verify(value, hash_))
