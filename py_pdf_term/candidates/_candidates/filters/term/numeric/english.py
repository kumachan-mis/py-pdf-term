from py_pdf_term._common.data import Term
from py_pdf_term.tokenizer import Token
from py_pdf_term.tokenizer.langs import EnglishTokenClassifier

from ..base import BaseEnglishCandidateTermFilter


class EnglishNumericFilter(BaseEnglishCandidateTermFilter):
    def __init__(self) -> None:
        self._classifier = EnglishTokenClassifier()

    def is_candidate(self, scoped_term: Term) -> bool:
        return not self._is_numeric_phrase(scoped_term)

    def _is_numeric_phrase(self, scoped_term: Term) -> bool:
        def is_numeric_or_meaningless(token: Token) -> bool:
            return token.pos == "NUM" or self._classifier.is_meaningless(token)

        return all(map(is_numeric_or_meaningless, scoped_term.tokens))
