import re

from ..base import BaseJapaneseCandidateTermFilter
from py_pdf_term.tokenizer import Morpheme
from py_pdf_term.tokenizer.langs import JapaneseMorphemeClassifier
from py_pdf_term._common.data import Term
from py_pdf_term._common.consts import (
    HIRAGANA_REGEX,
    KATAKANA_REGEX,
    ALPHABET_REGEX,
    NUMBER_REGEX,
)


PHONETIC_REGEX = rf"(?:{HIRAGANA_REGEX}|{KATAKANA_REGEX}|{ALPHABET_REGEX})"


class JapaneseSymbolLikeFilter(BaseJapaneseCandidateTermFilter):
    def __init__(self) -> None:
        self._classifier = JapaneseMorphemeClassifier()
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
            and not self._phonetic_morpheme_appears_continuously(scoped_term)
        )

    def _is_phonetic_or_meaningless_term(self, scoped_term: Term) -> bool:
        def is_phonetic_or_meaningless_morpheme(morpheme: Morpheme) -> bool:
            is_phonetic = self._phonetic_regex.fullmatch(str(morpheme)) is not None
            is_meaningless = self._classifier.is_meaningless(morpheme)
            return is_phonetic or is_meaningless

        return all(map(is_phonetic_or_meaningless_morpheme, scoped_term.morphemes))

    def _is_indexed_phonetic(self, scoped_term: Term) -> bool:
        return self._indexed_phonetic_regex.fullmatch(str(scoped_term)) is not None

    def _phonetic_morpheme_appears_continuously(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def phonetic_morpheme_appears_continuously_at(i: int) -> bool:
            if i == num_morphemes - 1:
                return False

            morpheme_str = str(scoped_term.morphemes[i])
            next_morpheme_str = str(scoped_term.morphemes[i + 1])
            return (
                self._phonetic_regex.fullmatch(morpheme_str) is not None
                and self._phonetic_regex.fullmatch(next_morpheme_str) is not None
            )

        return any(map(phonetic_morpheme_appears_continuously_at, range(num_morphemes)))
