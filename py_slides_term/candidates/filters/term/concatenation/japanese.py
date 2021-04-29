import re

from ..base import BaseJapaneseCandidateTermFilter
from py_slides_term.morphemes import JapaneseMorphemeClassifier
from py_slides_term.share.data import Term
from py_slides_term.share.consts import HIRAGANA_REGEX, KATAKANA_REGEX


PHONETIC_REGEX = rf"{HIRAGANA_REGEX}|{KATAKANA_REGEX}|[A-Za-z\-]"


class JapaneseConcatenationFilter(BaseJapaneseCandidateTermFilter):
    # public
    def __init__(self):
        self._classifier = JapaneseMorphemeClassifier()

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

        def norn_or_postfix_appears_at(i: int) -> bool:
            return scoped_term.morphemes[i].pos in {"名詞", "接尾辞"}

        induces_should_be_norn = [
            i - 1
            for i in range(num_morphemes)
            if i > 0
            and self._classifier.is_modifying_particle(scoped_term.morphemes[i])
        ] + [num_morphemes - 1]

        return all(map(norn_or_postfix_appears_at, induces_should_be_norn))

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
