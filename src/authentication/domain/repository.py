from typing import Protocol
from src.authentication.domain import model


class UserRepository(Protocol):
    def add(self, user: model.User):
        ...

    def get(self, id: int) -> model.User | None:
        ...

    def get_by_email(self, email: str) -> model.User | None:
        ...


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


class FakeRepository:
    def __init__(self, users) -> None:
        self._users = set(users)

    def add(self, user: model.User):
        self._users.add(user)

    def get(self, id: int) -> model.User | None:
        return next((u for u in self._users if u.id == id), None)

    def get_by_email(self, email: str) -> model.User | None:
        return next((u for u in self._users if u.email == email), None)