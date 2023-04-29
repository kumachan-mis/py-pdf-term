from abc import ABCMeta, abstractmethod
from typing import BinaryIO, Literal


class BaseBinaryOpener(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def open(self, file: str, mode: Literal["rb", "wb"]) -> BinaryIO:
        raise NotImplementedError(f"{self.__class__.__name__}.open()")
