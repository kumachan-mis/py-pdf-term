from typing import BinaryIO, Callable

from ..base import BaseMapper


class BinaryOpenerMapper(BaseMapper[Callable[[str, str], BinaryIO]]):
    @classmethod
    def default_mapper(cls) -> "BinaryOpenerMapper":
        default_mapper = cls()
        default_mapper.add("python.open", open)  # type:ignore
        return default_mapper
