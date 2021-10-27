from typing import Type

from py_pdf_term.candidates.splitters import (
    BaseSplitter,
    RepeatSplitter,
    SymbolNameSplitter,
)

from ..base import BaseMapper
from ..consts import PACKAGE_NAME


class SplitterMapper(BaseMapper[Type[BaseSplitter]]):
    @classmethod
    def default_mapper(cls) -> "SplitterMapper":
        default_mapper = cls()

        splitter_clses = [SymbolNameSplitter, RepeatSplitter]
        for splitter_cls in splitter_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{splitter_cls.__name__}", splitter_cls)

        return default_mapper
