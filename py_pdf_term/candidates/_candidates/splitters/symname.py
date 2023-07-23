import re

from py_pdf_term._common.consts import ALPHABET_REGEX, NUMBER_REGEX
from py_pdf_term.tokenizers import Term

from ..classifiers import BaseTokenClassifier
from .base import BaseSplitter


class SymbolNameSplitter(BaseSplitter):
    """Splitter to split down a symbol at the end of a term. For example, given
    "Programming Language 2", this splitter splits it into "Programming Language" and
    "2", and then "2" is ignored as a meaningless term.

    Args
    ----
        classifiers:
            List of token classifiers to classify tokens into specific categories.
            If None, the default classifiers are used. The default classifiers are
            JapaneseTokenClassifier and EnglishTokenClassifier.
    """

    def __init__(self, classifiers: list[BaseTokenClassifier] | None = None) -> None:
        super().__init__(classifiers=classifiers)

    def split(self, term: Term) -> list[Term]:
        num_tokens = len(term.tokens)
        if num_tokens < 2:
            return [term]

        regex = re.compile(rf"{ALPHABET_REGEX}|{NUMBER_REGEX}+|\-")
        last_str = str(term.tokens[-1])
        second_last_str = str(term.tokens[-2])

        if not regex.fullmatch(last_str) or regex.fullmatch(second_last_str):
            return [term]

        nonsym_tokens = term.tokens[:-1]
        nonsym_term = Term(nonsym_tokens, term.fontsize, term.ncolor, term.augmented)
        return [nonsym_term]
