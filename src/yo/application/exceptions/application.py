class ApplicationError(Exception):
    def __init__(self, message: str, *args) -> None:
        self._message = message
        super().__init__(args)

    @property
    def message(self):
        return self._message
