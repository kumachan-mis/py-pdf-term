import re

from py_pdf_term._common.consts import ALPHABET_REGEX
from py_pdf_term._common.data import Term
from py_pdf_term.tokenizer.langs import EnglishTokenClassifier

from ..base import BaseEnglishCandidateTermFilter

PHONETIC_REGEX = ALPHABET_REGEX


class EnglishConcatenationFilter(BaseEnglishCandidateTermFilter):
    def __init__(self) -> None:
        self._classifier = EnglishTokenClassifier()

    def is_candidate(self, scoped_term: Term) -> bool:
        return (
            self._is_norn_phrase(scoped_term)
            and not self._has_invalid_connector_symbol(scoped_term)
            and not self._has_invalid_adposition(scoped_term)
            and not self._has_invalid_adjective(scoped_term)
        )

    def _is_norn_phrase(self, scoped_term: Term) -> bool:
        num_tokens = len(scoped_term.tokens)

        def norn_appears_at(i: int) -> bool:
            token = scoped_term.tokens[i]
            if token.pos in {"NOUN", "PROPN", "NUM"}:
                return True
            elif token.pos == "VERB":
                return token.category == "VBG"

            return False

        induces_should_be_norn = [
            i - 1
            for i in range(1, num_tokens)
            if self._classifier.is_adposition(scoped_term.tokens[i])
        ] + [num_tokens - 1]

        return all(map(norn_appears_at, induces_should_be_norn))

    def _has_invalid_connector_symbol(self, scoped_term: Term) -> bool:
        num_tokens = len(scoped_term.tokens)

        def invalid_connector_symbol_appears_at(i: int) -> bool:
            if not self._classifier.is_connector_symbol(scoped_term.tokens[i]):
                return False
            return (
                i == 0
                or i == num_tokens - 1
                or self._classifier.is_connector_symbol(scoped_term.tokens[i - 1])
                or self._classifier.is_connector_symbol(scoped_term.tokens[i + 1])
            )

        return any(map(invalid_connector_symbol_appears_at, range(num_tokens)))

    def _has_invalid_adposition(self, scoped_term: Term) -> bool:
        num_tokens = len(scoped_term.tokens)
        phonetic_regex = re.compile(PHONETIC_REGEX)

        def invalid_adposition_appears_at(i: int) -> bool:
            if not self._classifier.is_adposition(scoped_term.tokens[i]):
                return False
            return (
                i == 0
                or i == num_tokens - 1
                or self._classifier.is_adposition(scoped_term.tokens[i - 1])
                or self._classifier.is_adposition(scoped_term.tokens[i + 1])
                or self._classifier.is_symbol(scoped_term.tokens[i - 1])
                or self._classifier.is_symbol(scoped_term.tokens[i + 1])
                or phonetic_regex.fullmatch(str(scoped_term.tokens[i - 1])) is not None
                or phonetic_regex.fullmatch(str(scoped_term.tokens[i + 1])) is not None
            )

        return any(map(invalid_adposition_appears_at, range(num_tokens)))

    def _has_invalid_adjective(self, scoped_term: Term) -> bool:
        num_tokens = len(scoped_term.tokens)

        def invalid_adjective_or_appears_at(i: int) -> bool:
            token = scoped_term.tokens[i]
            if not (
                token.pos == "ADJ" or (token.pos == "VERB" and token.category == "VBN")
            ):
                return False

            return (
                i == num_tokens - 1
                or scoped_term.tokens[i + 1].pos
                not in {"NOUN", "PROPN", "ADJ", "VERB", "SYM"}
                # No line break
            )

        return any(map(invalid_adjective_or_appears_at, range(num_tokens)))
