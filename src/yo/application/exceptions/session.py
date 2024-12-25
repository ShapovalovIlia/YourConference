from .application import ApplicationError


class UknownSessionIdError(ApplicationError):
    def __init__(self, message, *args) -> None:
        super().__init__(message, *args)
