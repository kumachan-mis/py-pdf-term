import re

from .base import BaseCandidateTermFilter
from py_slides_term.share.data import Term
from py_slides_term.share.consts import HIRAGANA_REGEX, KATAKANA_REGEX, KANJI_REGEX


JAPANESE_REGEX = rf"({HIRAGANA_REGEX}|{KATAKANA_REGEX}|{KANJI_REGEX})"
ENGLISH_REGEX = r"[A-Za-z ]"
PHONETIC_REGEX = rf"{HIRAGANA_REGEX}|{KATAKANA_REGEX}|[A-Za-z\-]"


class SymbolLikeFilter(BaseCandidateTermFilter):
    # public
    def __init__(self):
        pass

    def inscope(self, term: Term) -> bool:
        regex = re.compile(rf"({JAPANESE_REGEX}|{ENGLISH_REGEX}|\-)+")
        return regex.fullmatch(str(term)) is not None

    def is_candidate(self, scoped_term: Term) -> bool:
        return not self._has_phonetic_symbol(scoped_term)

    # private
    def _has_phonetic_symbol(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)
        phonetic_regex = re.compile(PHONETIC_REGEX)

        if num_morphemes == 1:
            morpheme_str = str(scoped_term.morphemes[0])
            return phonetic_regex.fullmatch(morpheme_str) is not None

        def phonetic_char_appears_continuously_at(i: int) -> bool:
            if i == num_morphemes - 1:
                return False

            morpheme_str = str(scoped_term.morphemes[i])
            next_morpheme_str = str(scoped_term.morphemes[i + 1])
            return (
                phonetic_regex.fullmatch(morpheme_str) is not None
                and phonetic_regex.fullmatch(next_morpheme_str) is not None
            )

        return any(map(phonetic_char_appears_continuously_at, range(num_morphemes)))
