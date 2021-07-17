import re
from typing import List

from .base import BaseSplitter
from py_pdf_term._common.data import Term
from py_pdf_term._common.consts import ALPHABET_REGEX, NUMBER_REGEX


class SymbolNameSplitter(BaseSplitter):
    def __init__(self) -> None:
        pass

    def split(self, term: Term) -> List[Term]:
        num_morphemes = len(term.morphemes)
        if num_morphemes < 2:
            return [term]

        regex = re.compile(rf"{ALPHABET_REGEX}|{NUMBER_REGEX}+|\-")
        last_str = str(term.morphemes[len(term.morphemes) - 1])
        second_last_str = str(term.morphemes[len(term.morphemes) - 2])

        if not regex.fullmatch(last_str) or regex.fullmatch(second_last_str):
            return [term]

        nonsym_morphemes = term.morphemes[: num_morphemes - 1]
        nonsym_term = Term(nonsym_morphemes, term.fontsize, term.ncolor, term.augmented)
        return [nonsym_term]
