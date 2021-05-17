import re
from typing import List

from .base import BaseSplitter
from ..filters import FilterCombiner
from py_slides_term.share.data import Term
from py_slides_term.share.consts import ALPHABET_REGEX


class SymbolNameSplitter(BaseSplitter):
    # public
    def __init__(self, candidate_filter: FilterCombiner):
        self._filter = candidate_filter

    def split(self, term: Term) -> List[Term]:
        num_morphemes = len(term.morphemes)
        if num_morphemes < 2:
            return [term]

        regex = re.compile(rf"{ALPHABET_REGEX}|\-")
        last_str = str(term.morphemes[len(term.morphemes) - 1])
        second_last_str = str(term.morphemes[len(term.morphemes) - 2])

        if not regex.fullmatch(last_str) or regex.fullmatch(second_last_str):
            return [term]

        nonsym_morphemes = term.morphemes[: num_morphemes - 1]
        sym_morphemes = [term.morphemes[num_morphemes - 1]]

        nonsym_term = Term(nonsym_morphemes, term.fontsize, term.ncolor, term.augmented)
        sym_term = Term(sym_morphemes, term.fontsize, term.ncolor, term.augmented)

        if not self._filter.is_candidate(nonsym_term):
            return [term]

        splitted_terms = [nonsym_term]
        if self._filter.is_candidate(sym_term):
            splitted_terms.append(sym_term)

        return splitted_terms
