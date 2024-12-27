from typing import Self

from py_pdf_term._common.consts import PACKAGE_NAME
from py_pdf_term.candidates.splitters import (
    BaseSplitter,
    RepeatSplitter,
    SymbolNameSplitter,
)

from ..base import BaseMapper


class SplitterMapper(BaseMapper[type[BaseSplitter]]):
    """Mapper to find splitter classes."""

    @classmethod
    def default_mapper(cls) -> Self:
        default_mapper = cls()

        splitter_clses: list[type[BaseSplitter]] = [SymbolNameSplitter, RepeatSplitter]
        for splitter_cls in splitter_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{splitter_cls.__name__}", splitter_cls)

        return default_mapper
