from .application import ApplicationError


class UserAlreadyExistsError(ApplicationError):
    def __init__(self, message, *args) -> None:
        super().__init__(message, *args)


class WrongPasswordOrUsernameError(ApplicationError):
    def __init__(self, message, *args) -> None:
        super().__init__(message, *args)


class UserNotFoundError(ApplicationError):
    def __init__(self, message, *args) -> None:
        super().__init__(message, *args)
