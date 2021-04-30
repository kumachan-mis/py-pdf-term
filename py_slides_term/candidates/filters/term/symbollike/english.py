import re

from ..base import BaseEnglishCandidateTermFilter
from py_slides_term.morphemes import BaseMorpheme, EnglishMorphemeClassifier
from py_slides_term.share.data import Term
from py_slides_term.share.consts import ALPHABET_REGEX


PHONETIC_REGEX = ALPHABET_REGEX


class EnglishSymbolLikeFilter(BaseEnglishCandidateTermFilter):
    # public
    def __init__(self):
        self._classifier = EnglishMorphemeClassifier()

    def is_candidate(self, scoped_term: Term) -> bool:
        return (
            str(scoped_term) != ""
            and not self._is_phonetic_or_meaningless_term(scoped_term)
            and not self._phonetic_morpheme_appears_continuously(scoped_term)
        )

    # private
    def _is_phonetic_or_meaningless_term(self, scoped_term: Term) -> bool:
        phonetic_regex = re.compile(PHONETIC_REGEX)

        def is_phonetic_or_meaningless_morpheme(morpheme: BaseMorpheme) -> bool:
            is_phonetic = phonetic_regex.fullmatch(str(morpheme)) is not None
            is_meaningless = self._classifier.is_meaningless(morpheme)
            return is_phonetic or is_meaningless

        return all(map(is_phonetic_or_meaningless_morpheme, scoped_term.morphemes))

    def _phonetic_morpheme_appears_continuously(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)
        phonetic_regex = re.compile(PHONETIC_REGEX)

        def phonetic_morpheme_appears_continuously_at(i: int) -> bool:
            if i == num_morphemes - 1:
                return False

            morpheme_str = str(scoped_term.morphemes[i])
            next_morpheme_str = str(scoped_term.morphemes[i + 1])
            return (
                phonetic_regex.fullmatch(morpheme_str) is not None
                and phonetic_regex.fullmatch(next_morpheme_str) is not None
            )

        return any(map(phonetic_morpheme_appears_continuously_at, range(num_morphemes)))
