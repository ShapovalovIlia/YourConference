from abc import ABC, abstractmethod


class ApplicationError(Exception, ABC):
    @property
    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError
