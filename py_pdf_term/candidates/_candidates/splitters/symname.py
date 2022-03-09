import re
from typing import List, Optional

from py_pdf_term._common.consts import ALPHABET_REGEX, NUMBER_REGEX
from py_pdf_term._common.data import Term

from .base import BaseSplitter
from ..classifiers import BaseTokenClassifier


class SymbolNameSplitter(BaseSplitter):
    def __init__(self, classifiers: Optional[List[BaseTokenClassifier]] = None) -> None:
        super().__init__(classifiers=classifiers)

    def split(self, term: Term) -> List[Term]:
        num_tokens = len(term.tokens)
        if num_tokens < 2:
            return [term]

        regex = re.compile(rf"{ALPHABET_REGEX}|{NUMBER_REGEX}+|\-")
        last_str = str(term.tokens[len(term.tokens) - 1])
        second_last_str = str(term.tokens[len(term.tokens) - 2])

        if not regex.fullmatch(last_str) or regex.fullmatch(second_last_str):
            return [term]

        nonsym_tokens = term.tokens[: num_tokens - 1]
        nonsym_term = Term(nonsym_tokens, term.fontsize, term.ncolor, term.augmented)
        return [nonsym_term]
