import re

from .base import BaseCandidateTermFilter
from py_slides_term.morphemes import (
    JapaneseMorphemeClassifier,
    EnglishMorphemeClassifier,
)
from py_slides_term.share.data import Term
from py_slides_term.share.consts import HIRAGANA_REGEX, KATAKANA_REGEX, KANJI_REGEX


JAPANESE_REGEX = rf"({HIRAGANA_REGEX}|{KATAKANA_REGEX}|{KANJI_REGEX})"
ENGLISH_REGEX = r"[A-Za-z ]"
PHONETIC_REGEX = rf"{HIRAGANA_REGEX}|{KATAKANA_REGEX}|[A-Za-z\-]"


class JapaneseConcatenationFilter(BaseCandidateTermFilter):
    # public
    def __init__(self):
        self._classifier = JapaneseMorphemeClassifier()

    def inscope(self, term: Term) -> bool:
        ja_regex = re.compile(rf"{JAPANESE_REGEX}+")
        ja_en_regex = re.compile(rf"({JAPANESE_REGEX}|{ENGLISH_REGEX}|\-)+")
        return ja_en_regex.fullmatch(str(term)) is not None and any(
            map(
                lambda morpheme: ja_regex.fullmatch(morpheme.pos) is not None,
                term.morphemes,
            )
        )

    def is_candidate(self, scoped_term: Term) -> bool:
        return (
            self._is_norn_phrase(scoped_term)
            and not self._has_invalid_connector_symbol(scoped_term)
            and not self._has_invalid_modifying_particle(scoped_term)
            and not self._has_invalid_prefix(scoped_term)
            and not self._has_invalid_postfix(scoped_term)
            and not self._has_adjverb_without_nounization(scoped_term)
        )

    # private
    def _is_norn_phrase(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)
        return scoped_term.morphemes[num_morphemes - 1].pos in {"名詞", "接尾辞"}

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

    def _has_invalid_modifying_particle(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)
        phonetic_regex = re.compile(PHONETIC_REGEX)

        def invalid_modifying_particle_appears_at(i: int) -> bool:
            if not self._classifier.is_modifying_particle(scoped_term.morphemes[i]):
                return False
            return (
                i == 0
                or i == num_morphemes - 1
                or scoped_term.morphemes[i - 1].pos in {"助詞", "補助記号"}
                or scoped_term.morphemes[i + 1].pos in {"助詞", "補助記号"}
                or phonetic_regex.fullmatch(str(scoped_term.morphemes[i - 1]))
                is not None
                or phonetic_regex.fullmatch(str(scoped_term.morphemes[i + 1]))
                is not None
            )

        return any(map(invalid_modifying_particle_appears_at, range(num_morphemes)))

    def _has_invalid_prefix(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def invalid_prefix_appears_at(i: int) -> bool:
            if scoped_term.morphemes[i].pos != "接頭辞":
                return False
            return i == num_morphemes - 1 or scoped_term.morphemes[i + 1].pos not in {
                "名詞",
                "形状詞",
            }

        return any(map(invalid_prefix_appears_at, range(num_morphemes)))

    def _has_invalid_postfix(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def invalid_postfix_appears_at(i: int) -> bool:
            if scoped_term.morphemes[i].pos != "接尾辞":
                return False
            return i == 0 or scoped_term.morphemes[i - 1].pos not in {"名詞", "形状詞"}

        return any(map(invalid_postfix_appears_at, range(num_morphemes)))

    def _has_adjverb_without_nounization(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def adjverb_without_nounization_appears_at(i: int) -> bool:
            if scoped_term.morphemes[i].pos not in {"動詞", "形容詞"}:
                return False
            return i == num_morphemes - 1 or scoped_term.morphemes[i + 1].pos != "接尾辞"

        return any(map(adjverb_without_nounization_appears_at, range(num_morphemes)))


class EnglishConcatenationFilter(BaseCandidateTermFilter):
    # public
    def __init__(self):
        self._classifier = EnglishMorphemeClassifier()

    def inscope(self, term: Term) -> bool:
        regex = re.compile(r"[A-Za-z\- ]+")
        return regex.fullmatch(str(term)) is not None and all(
            map(
                lambda morpheme: regex.fullmatch(morpheme.pos) is not None,
                term.morphemes,
            )
        )

    def is_candidate(self, scoped_term: Term) -> bool:
        return (
            self._is_norn_phrase(scoped_term)
            and not self._has_invalid_connector_symbol(scoped_term)
            and not self._has_invalid_adposition(scoped_term)
            and not self._has_invalid_adjective(scoped_term)
            and not self._has_invalid_participle(scoped_term)
        )

    # private
    def _is_norn_phrase(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def norn_appears_at(i: int) -> bool:
            morpheme = scoped_term.morphemes[i]
            if morpheme.pos in {"NOUN", "PROPN"}:
                return True
            elif morpheme.pos == "VERB":
                return morpheme.category == "VBG"

            return False

        induces_should_be_norn = [
            i - 1
            for i in range(num_morphemes)
            if i > 0 and scoped_term.morphemes[i].pos == "ADP"
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

        def invalid_adposition_appears_at(i: int) -> bool:
            if scoped_term.morphemes[i].pos != "ADP":
                return False

            return (
                i == 0
                or i == num_morphemes - 1
                or scoped_term.morphemes[i - 1].pos == "ADP"
                or scoped_term.morphemes[i + 1].pos == "ADP"
            )

        return any(map(invalid_adposition_appears_at, range(num_morphemes)))

    def _has_invalid_adjective(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def invalid_adjective_appears_at(i: int) -> bool:
            if scoped_term.morphemes[i].pos != "VERB":
                return False

            valid_part_of_speeches = {"NOUN", "PROPN", "ADJ", "VERB", "SYM"}
            return (
                i == num_morphemes - 1
                or scoped_term.morphemes[i + 1].pos not in valid_part_of_speeches
            )

        return any(map(invalid_adjective_appears_at, range(num_morphemes)))

    def _has_invalid_participle(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def invalid_participle_appears_at(i: int) -> bool:
            if scoped_term.morphemes[i].pos != "ADJ":
                return False

            valid_part_of_speeches = {"NOUN", "PROPN", "ADJ", "VERB", "SYM"}
            return (
                i == num_morphemes - 1
                or scoped_term.morphemes[i + 1].pos not in valid_part_of_speeches
            )

        return any(map(invalid_participle_appears_at, range(num_morphemes)))
