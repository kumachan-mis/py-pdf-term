import re

from py_pdf_term._common.consts import ALPHABET_REGEX, NUMBER_REGEX
from py_pdf_term._common.data import Term
from py_pdf_term.tokenizer import Token
from py_pdf_term.tokenizer.langs import EnglishTokenClassifier

from ..base import BaseEnglishCandidateTermFilter

PHONETIC_REGEX = ALPHABET_REGEX


class EnglishSymbolLikeFilter(BaseEnglishCandidateTermFilter):
    def __init__(self) -> None:
        self._classifier = EnglishTokenClassifier()
        self._phonetic_regex = re.compile(PHONETIC_REGEX)
        self._indexed_phonetic_regex = re.compile(
            rf"({PHONETIC_REGEX}{NUMBER_REGEX}+)+{PHONETIC_REGEX}?"
            + "|"
            + rf"({NUMBER_REGEX}+{PHONETIC_REGEX})+({NUMBER_REGEX}+)?"
        )

    def is_candidate(self, scoped_term: Term) -> bool:
        return (
            not self._is_phonetic_or_meaningless_term(scoped_term)
            and not self._is_indexed_phonetic(scoped_term)
            and not self._phonetic_token_appears_continuously(scoped_term)
        )

    def _is_phonetic_or_meaningless_term(self, scoped_term: Term) -> bool:
        def is_phonetic_or_meaningless_token(token: Token) -> bool:
            is_phonetic = self._phonetic_regex.fullmatch(str(token)) is not None
            is_meaningless = self._classifier.is_meaningless(token)
            return is_phonetic or is_meaningless

        return all(map(is_phonetic_or_meaningless_token, scoped_term.tokens))

    def _is_indexed_phonetic(self, scoped_term: Term) -> bool:
        return self._indexed_phonetic_regex.fullmatch(str(scoped_term)) is not None

    def _phonetic_token_appears_continuously(self, scoped_term: Term) -> bool:
        num_tokens = len(scoped_term.tokens)

        def phonetic_token_appears_continuously_at(i: int) -> bool:
            if i == num_tokens - 1:
                return False

            token_str = str(scoped_term.tokens[i])
            next_token_str = str(scoped_term.tokens[i + 1])
            return (
                self._phonetic_regex.fullmatch(token_str) is not None
                and self._phonetic_regex.fullmatch(next_token_str) is not None
            )

        return any(map(phonetic_token_appears_continuously_at, range(num_tokens)))
