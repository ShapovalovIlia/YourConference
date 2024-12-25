from .application import ApplicationError


class PermissionError(ApplicationError):
    def __init__(self, message, *args) -> None:
        super().__init__(message, *args)
