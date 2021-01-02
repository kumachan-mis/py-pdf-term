import re

from .base import BaseCandidateTermFilter
from pdf_slides_term.share.data import Term
from pdf_slides_term.share.consts import HIRAGANA_REGEX, KATAKANA_REGEX, KANJI_REGEX


class ConcatenationFilter(BaseCandidateTermFilter):
    def __init__(self):
        pass

    def inscope(self, term: Term) -> bool:
        japanese_pattern = rf"({HIRAGANA_REGEX}|{KATAKANA_REGEX}|{KANJI_REGEX})"
        english_pattern = r"[A-Za-z\- ]"
        regex = re.compile(rf"({japanese_pattern}|{english_pattern})+")
        return regex.fullmatch(str(term)) is not None

    def is_candidate(self, scoped_term: Term) -> bool:
        return (
            not self._has_invalid_connector_symbol(scoped_term)
            and not self._has_invalid_modifying_particle(scoped_term)
            and not self._has_invalid_prefix(scoped_term)
            and not self._has_adjverb_without_nounization(scoped_term)
        )

    def _has_invalid_connector_symbol(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def invalid_connector_symbol_appears_at(i: int) -> bool:
            if scoped_term.morphemes[i].pos != "記号":
                return False
            return (
                i == 0
                or i == num_morphemes - 1
                or scoped_term.morphemes[i - 1].pos == "記号"
                or scoped_term.morphemes[i + 1].pos == "記号"
            )

        return any(map(invalid_connector_symbol_appears_at, range(num_morphemes)))

    def _has_invalid_modifying_particle(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)
        phonetic_regex = re.compile(rf"({HIRAGANA_REGEX}|{KATAKANA_REGEX}|[A-Za-z\-])")

        def invalid_modifying_particle_appears_at(i: int) -> bool:
            if scoped_term.morphemes[i].pos != "助詞":
                return False
            return (
                i == 0
                or i == num_morphemes - 1
                or scoped_term.morphemes[i - 1].pos != "名詞"
                or scoped_term.morphemes[i + 1].pos != "名詞"
                or phonetic_regex.fullmatch(str(scoped_term.morphemes[i - 1]))
                is not None
                or phonetic_regex.fullmatch(str(scoped_term.morphemes[i + 1]))
                is not None
            )

        return any(map(invalid_modifying_particle_appears_at, range(num_morphemes)))

    def _has_invalid_prefix(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def invalid_prefix_appears_at(i: int) -> bool:
            if scoped_term.morphemes[i].pos != "接頭詞":
                return False
            return i == num_morphemes - 1 or (
                scoped_term.morphemes[i].category == "名詞接続"
                and scoped_term.morphemes[i + 1].pos != "名詞"
            )

        return any(map(invalid_prefix_appears_at, range(num_morphemes)))

    def _has_adjverb_without_nounization(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def adjverb_without_nounization_appears_at(i: int) -> bool:
            if scoped_term.morphemes[i].pos not in {"動詞", "形容詞"}:
                return False
            return i == num_morphemes - 1 or not (
                scoped_term.morphemes[i + 1].pos == "名詞"
                and scoped_term.morphemes[i + 1].category == "接尾"
                and scoped_term.morphemes[i + 1].subcategory == "特殊"
            )

        return any(map(adjverb_without_nounization_appears_at, range(num_morphemes)))
