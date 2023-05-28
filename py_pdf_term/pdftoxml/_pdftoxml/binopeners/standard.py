from typing import BinaryIO, Literal

from .base import BaseBinaryOpener


class StandardBinaryOpener(BaseBinaryOpener):
    """File opener with binary mode using the standard open function in Python."""

    def __init__(self) -> None:
        super().__init__()

    def open(self, file: str, mode: Literal["rb", "wb"]) -> BinaryIO:
        return open(file, mode)
