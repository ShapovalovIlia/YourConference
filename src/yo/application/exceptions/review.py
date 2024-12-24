from .application import ApplicationError


class ReviewAlreadyExistsError(ApplicationError):
    def __init__(self, message: str, *args):
        self._message = message
        super().__init__(args)

    @property
    def message(self):
        return self._message
