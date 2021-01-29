from typing import List

from .base import BaseSplitter
from ..filters import FilterCombiner
from py_slides_term.share.data import Term


class SymbolNameSplitter(BaseSplitter):
    # public
    def __init__(self, candidate_filter: FilterCombiner):
        self._filter = candidate_filter

    def split(self, term: Term) -> List[Term]:
        return [term]
