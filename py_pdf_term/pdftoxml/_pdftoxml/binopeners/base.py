from abc import ABCMeta, abstractmethod
from typing import BinaryIO, Literal


class BaseBinaryOpener(metaclass=ABCMeta):
    """Base class for file opener with binary mode."""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def open(self, file: str, mode: Literal["rb", "wb"]) -> BinaryIO:
        """Open a file with binary mode.

        Args
        ----
            file:
                Path to a file.
            mode:
                Mode to open the file.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.open()")
