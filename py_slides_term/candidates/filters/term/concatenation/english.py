import re

from ..base import BaseEnglishCandidateTermFilter
from py_slides_term.tokenizer import EnglishMorphemeClassifier
from py_slides_term.share.data import Term
from py_slides_term.share.consts import ALPHABET_REGEX


PHONETIC_REGEX = ALPHABET_REGEX


class EnglishConcatenationFilter(BaseEnglishCandidateTermFilter):
    def __init__(self) -> None:
        self._classifier = EnglishMorphemeClassifier()

    def is_candidate(self, scoped_term: Term) -> bool:
        return (
            self._is_norn_phrase(scoped_term)
            and not self._has_invalid_connector_symbol(scoped_term)
            and not self._has_invalid_adposition(scoped_term)
            and not self._has_invalid_adjective(scoped_term)
        )

    def _is_norn_phrase(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def norn_appears_at(i: int) -> bool:
            morpheme = scoped_term.morphemes[i]
            if morpheme.pos in {"NOUN", "PROPN", "NUM"}:
                return True
            elif morpheme.pos == "VERB":
                return morpheme.category == "VBG"

            return False

        induces_should_be_norn = [
            i - 1
            for i in range(1, num_morphemes)
            if self._classifier.is_adposition(scoped_term.morphemes[i])
        ] + [num_morphemes - 1]

        return all(map(norn_appears_at, induces_should_be_norn))

    def _has_invalid_connector_symbol(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def invalid_connector_symbol_appears_at(i: int) -> bool:
            if not self._classifier.is_connector_symbol(scoped_term.morphemes[i]):
                return False
            return (
                i == 0
                or i == num_morphemes - 1
                or self._classifier.is_connector_symbol(scoped_term.morphemes[i - 1])
                or self._classifier.is_connector_symbol(scoped_term.morphemes[i + 1])
            )

        return any(map(invalid_connector_symbol_appears_at, range(num_morphemes)))

    def _has_invalid_adposition(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)
        phonetic_regex = re.compile(PHONETIC_REGEX)

        def invalid_adposition_appears_at(i: int) -> bool:
            if not self._classifier.is_adposition(scoped_term.morphemes[i]):
                return False
            return (
                i == 0
                or i == num_morphemes - 1
                or self._classifier.is_adposition(scoped_term.morphemes[i - 1])
                or self._classifier.is_adposition(scoped_term.morphemes[i + 1])
                or self._classifier.is_symbol(scoped_term.morphemes[i - 1])
                or self._classifier.is_symbol(scoped_term.morphemes[i + 1])
                or phonetic_regex.fullmatch(str(scoped_term.morphemes[i - 1]))
                is not None
                or phonetic_regex.fullmatch(str(scoped_term.morphemes[i + 1]))
                is not None
            )

        return any(map(invalid_adposition_appears_at, range(num_morphemes)))

    def _has_invalid_adjective(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def invalid_adjective_appears_at(i: int) -> bool:
            if scoped_term.morphemes[i].pos != "ADJ":
                return False

            valid_part_of_speeches = {"NOUN", "PROPN", "ADJ", "VERB", "SYM"}
            return (
                i == num_morphemes - 1
                or scoped_term.morphemes[i + 1].pos not in valid_part_of_speeches
            )

        return any(map(invalid_adjective_appears_at, range(num_morphemes)))
