from typing import List, Protocol
from src.authentication.domain.model import User


class UserRepository(Protocol):
    def add(self, user: User) -> None:
        ...

    def get(self, id: int) -> User | None:
        ...

    def get_by_email(self, email: str) -> User | None:
        ...


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


class FakeUserRepository:
    def __init__(self, users: List[User]) -> None:
        self._users = set(users)

    def add(self, user: User) -> None:
        self._users.add(user)

    def get(self, id: int) -> User | None:
        return next((u for u in self._users if u.id == id), None)

    def get_by_email(self, email: str) -> User | None:
        return next((u for u in self._users if u.email == email), None)
