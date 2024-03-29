
from src.authentication.domain import model


class UserSqlAlchemyRepository:
    def __init__(self, session):
        self.session = session

    def add(self, user: model.User) -> None:
        self.session.add(user)
        self.session.commit()

    def get(self, id: int) -> model.User | None:
        return self.session.query(model.User).filter_by(id=id).first()

    def get_by_email(self, email: str) -> model.User | None:
        return self.session.query(model.User).filter_by(email=email).first()
