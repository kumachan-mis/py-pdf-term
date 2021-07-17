import re

from ..base import BaseJapaneseCandidateTermFilter
from py_pdf_term.tokenizer.langs import JapaneseMorphemeClassifier
from py_pdf_term._common.data import Term
from py_pdf_term._common.consts import HIRAGANA_REGEX, KATAKANA_REGEX, ALPHABET_REGEX


PHONETIC_REGEX = rf"{HIRAGANA_REGEX}|{KATAKANA_REGEX}|{ALPHABET_REGEX}"


class JapaneseConcatenationFilter(BaseJapaneseCandidateTermFilter):
    def __init__(self) -> None:
        self._classifier = JapaneseMorphemeClassifier()

    def is_candidate(self, scoped_term: Term) -> bool:
        return (
            self._is_norn_phrase(scoped_term)
            and not self._has_invalid_connector_symbol(scoped_term)
            and not self._has_invalid_modifying_particle(scoped_term)
            and not self._has_invalid_prefix(scoped_term)
            and not self._has_invalid_postfix(scoped_term)
            and not self._has_invalid_adjective(scoped_term)
            and not self._has_invalid_verb(scoped_term)
        )

    def _is_norn_phrase(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def norn_or_postfix_appears_at(i: int) -> bool:
            return scoped_term.morphemes[i].pos in {"名詞", "記号", "接尾辞"}

        induces_should_be_norn = [
            i - 1
            for i in range(1, num_morphemes)
            if self._classifier.is_modifying_particle(scoped_term.morphemes[i])
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
                or scoped_term.morphemes[i - 1].pos == "助詞"
                or scoped_term.morphemes[i + 1].pos == "助詞"
                or self._classifier.is_symbol(scoped_term.morphemes[i - 1])
                or self._classifier.is_symbol(scoped_term.morphemes[i + 1])
                or phonetic_regex.fullmatch(str(scoped_term.morphemes[i - 1]))
                is not None
                or phonetic_regex.fullmatch(str(scoped_term.morphemes[i + 1]))
                is not None
            )

        return any(map(invalid_modifying_particle_appears_at, range(num_morphemes)))

    def _has_invalid_prefix(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def invalid_prefix_appears_at(i: int) -> bool:
            morpheme = scoped_term.morphemes[i]
            if morpheme.pos != "接頭辞":
                return False
            return (
                i == num_morphemes - 1
                or scoped_term.morphemes[i + 1].pos not in {"名詞", "記号", "形状詞"}
                # No line break
            )

        return any(map(invalid_prefix_appears_at, range(num_morphemes)))

    def _has_invalid_postfix(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def invalid_postfix_appears_at(i: int) -> bool:
            morpheme = scoped_term.morphemes[i]
            if morpheme.pos != "接尾辞":
                return False
            return (
                i == 0
                or scoped_term.morphemes[i - 1].pos
                not in {"名詞", "記号", "形状詞", "動詞", "形容詞"}
                # No line break
            )

        return any(map(invalid_postfix_appears_at, range(num_morphemes)))

    def _has_invalid_adjective(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def invalid_adjective_appears_at(i: int) -> bool:
            morpheme = scoped_term.morphemes[i]
            if morpheme.pos not in {"形状詞", "形容詞"}:
                return False
            return (
                morpheme.category == ""
                or i == num_morphemes - 1
                or scoped_term.morphemes[i + 1].pos
                not in {"名詞", "記号", "接尾辞", "形状詞", "形容詞"}
            )

        return any(map(invalid_adjective_appears_at, range(num_morphemes)))

    def _has_invalid_verb(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def invalid__verb_appears_at(i: int) -> bool:
            morpheme = scoped_term.morphemes[i]
            if morpheme.pos != "動詞":
                return False
            return (
                i == num_morphemes - 1
                or scoped_term.morphemes[i + 1].pos not in {"接尾辞", "動詞"}
                # No line break
            )

        return any(map(invalid__verb_appears_at, range(num_morphemes)))
