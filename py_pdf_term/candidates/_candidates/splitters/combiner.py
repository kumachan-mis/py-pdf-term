from typing import List, Optional

from .base import BaseSplitter
from .symname import SymbolNameSplitter
from .repeat import RepeatSplitter
from py_pdf_term._common.data import Term


class SplitterCombiner:
    def __init__(self, splitters: Optional[List[BaseSplitter]] = None) -> None:
        if splitters is None:
            splitters = [SymbolNameSplitter(), RepeatSplitter()]

        self._splitters = splitters

    def split(self, term: Term) -> List[Term]:
        splitted_terms = [term]

        for splitter in self._splitters:
            start: List[Term] = []
            splitted_terms = sum(map(splitter.split, splitted_terms), start)

        return splitted_terms
