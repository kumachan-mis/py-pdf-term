import re

from .base import BaseCandidateTermFilter
from py_slides_term.morphemes import BaseMorpheme, MorphemeClassifier
from py_slides_term.share.data import Term
from py_slides_term.share.consts import HIRAGANA_REGEX, KATAKANA_REGEX, KANJI_REGEX


class ProperNounFilter(BaseCandidateTermFilter):
    def __init__(self):
        self._classifiter = MorphemeClassifier()

    def inscope(self, term: Term) -> bool:
        regex = re.compile(rf"({HIRAGANA_REGEX}|{KATAKANA_REGEX}|{KANJI_REGEX})+")
        return regex.fullmatch(str(term)) is not None

    def is_candidate(self, scoped_term: Term) -> bool:
        return not self._is_region_or_person(scoped_term)

    def _is_region_or_person(self, scoped_term: Term) -> bool:
        def is_region_or_person_morpheme(morpheme: BaseMorpheme) -> bool:
            return (
                morpheme.pos == "名詞"
                and morpheme.category == "固有名詞"
                and morpheme.subcategory in {"人名", "地名"}
            ) or self._classifiter.is_modifying_particle(morpheme)

        return all(map(is_region_or_person_morpheme, scoped_term.morphemes))
