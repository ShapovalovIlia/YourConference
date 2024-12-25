from .application import ApplicationError


class RegistrationAlreadyExistsError(ApplicationError):
    def __init__(self, message, *args) -> None:
        super().__init__(message, *args)


class RegistrationNotFoundError(ApplicationError):
    def __init__(self, message, *args) -> None:
        super().__init__(message, *args)
