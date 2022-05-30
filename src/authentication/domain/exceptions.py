class EmailNotUniqueError(Exception):
    def __init__(self, email: str, msg: str = "email already registered"):
        super().__init__(msg)
        self.msg = msg
        self.email = email

    def as_dict(self):
        return {"msg": self.msg, "email": self.email}


class UserNotFoundError(Exception):
    def __init__(self, msg: str = "user not found"):
        super().__init__(msg)
        self.msg = msg

    def as_dict(self):
        return {"msg": self.msg}


class PasswordValidationError(Exception):
    def __init__(self, msg: str = "password is invalid"):
        super().__init__(msg)
        self.msg = msg

    def as_dict(self):
        return {"msg": self.msg}
