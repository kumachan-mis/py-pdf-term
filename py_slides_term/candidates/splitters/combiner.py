from typing import List, Optional, cast

from .base import BaseSplitter
from .symname import SymbolNameSplitter
from .repeat import RepeatSplitter
from ..filters import FilterCombiner
from py_slides_term.share.data import Term


class SplitterCombiner:
    def __init__(
        self,
        splitters: Optional[List[BaseSplitter]] = None,
        candidate_filter: Optional[FilterCombiner] = None,
    ):
        if splitters is None:
            if candidate_filter is None:
                raise ValueError("both of 'splitters' and 'candidate_filter' are None")

            splitters = [
                SymbolNameSplitter(candidate_filter),
                RepeatSplitter(candidate_filter),
            ]

        self._splitters = splitters

    def split(self, term: Term) -> List[Term]:
        splitted_terms = [term]

        for splitter in self._splitters:
            splitted_terms = sum(
                map(splitter.split, splitted_terms), cast(List[Term], [])
            )

        return splitted_terms
