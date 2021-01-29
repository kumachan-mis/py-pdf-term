from typing import Type

from .base import BaseMapper
from py_slides_term.candidates import BaseSplitter, RepeatSplitter, SymbolNameSplitter


class SplitterMapper(BaseMapper[Type[BaseSplitter]]):
    @classmethod
    def default_mapper(cls):
        module_path = "py_slides_term.splitters"
        default_mapper = cls()

        splitter_clses = [RepeatSplitter, SymbolNameSplitter]
        for splitter_cls in splitter_clses:
            default_mapper.add(f"{module_path}.{splitter_cls.__name__}", splitter_cls)

        return default_mapper
