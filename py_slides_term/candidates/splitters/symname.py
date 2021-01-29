import re
from typing import List

from .base import BaseSplitter
from ..filters import FilterCombiner
from py_slides_term.share.data import Term


class SymbolNameSplitter(BaseSplitter):
    # public
    def __init__(self, candidate_filter: FilterCombiner):
        self._filter = candidate_filter

    def split(self, term: Term) -> List[Term]:
        num_morphemes = len(term.morphemes)
        if num_morphemes < 2:
            return [term]

        last_str = str(term.morphemes[len(term.morphemes) - 1])
        second_last_str = str(term.morphemes[len(term.morphemes) - 2])
        last_may_symbol = re.fullmatch(r"[A-Za-z]", last_str)
        second_last_may_symbol = re.fullmatch(r"[A-Za-z\-]", second_last_str)

        if not last_may_symbol or second_last_may_symbol:
            return [term]

        non_symbol_morphemes = term.morphemes[: num_morphemes - 1]
        symbol_morphemes = [term.morphemes[num_morphemes - 1]]
        non_symbol_term = Term(non_symbol_morphemes, term.fontsize, term.augmented)
        symbol_term = Term(symbol_morphemes, term.fontsize, term.augmented)

        if not self._filter.is_candidate(non_symbol_term):
            return [term]

        splitted_terms = [non_symbol_term]
        if self._filter.is_candidate(symbol_term):
            splitted_terms.append(symbol_term)

        return splitted_terms
