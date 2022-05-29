class EmailNotUniqueError(Exception):
    def __init__(self, email: str, msg: str = "email already registered"):
        super().__init__(msg)
        self.msg = msg
        self.email = email

    def as_dict(self):
        return {"msg": self.msg, "email": self.email}


class UserNotFoundError(Exception):
    def __init__(self, id_, msg: str = "user not found"):
        super().__init__(msg)
        self.user_id = id_
        self.msg = msg

    def as_dict(self):
        return {"msg": self.msg, "user_id": self.user_id}


class PasswordValidationError(Exception):
    def __init__(self, msg: str = "password is invalid"):
        super().__init__(msg)
        self.msg = msg

    def as_dict(self):
        return {"msg": self.msg}
