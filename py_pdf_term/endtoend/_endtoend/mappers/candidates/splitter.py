from typing import Type

from ..base import BaseMapper
from ..consts import PACKAGE_NAME
from py_pdf_term.candidates.splitters import (
    BaseSplitter,
    SymbolNameSplitter,
    RepeatSplitter,
)


class SplitterMapper(BaseMapper[Type[BaseSplitter]]):
    @classmethod
    def default_mapper(cls) -> "SplitterMapper":
        default_mapper = cls()

        splitter_clses = [SymbolNameSplitter, RepeatSplitter]
        for splitter_cls in splitter_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{splitter_cls.__name__}", splitter_cls)

        return default_mapper
