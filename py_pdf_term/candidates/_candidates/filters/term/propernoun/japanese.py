from ..base import BaseJapaneseCandidateTermFilter
from py_pdf_term.tokenizer import Morpheme
from py_pdf_term.tokenizer.langs import JapaneseMorphemeClassifier
from py_pdf_term._common.data import Term


class JapaneseProperNounFilter(BaseJapaneseCandidateTermFilter):
    def __init__(self) -> None:
        self._classifier = JapaneseMorphemeClassifier()

    def is_candidate(self, scoped_term: Term) -> bool:
        return not self._is_region_or_person(scoped_term)

    def _is_region_or_person(self, scoped_term: Term) -> bool:
        def is_region_or_person_morpheme(morpheme: Morpheme) -> bool:
            return (
                (
                    morpheme.pos == "名詞"
                    and morpheme.category == "固有名詞"
                    and morpheme.subcategory in {"人名", "地名"}
                )
                or self._classifier.is_modifying_particle(morpheme)
                or self._classifier.is_connector_symbol(morpheme)
            )

        return all(map(is_region_or_person_morpheme, scoped_term.morphemes))
