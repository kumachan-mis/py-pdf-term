from ..base import BaseEnglishCandidateTermFilter
from py_pdf_term.tokenizer import Morpheme
from py_pdf_term.tokenizer.langs import EnglishMorphemeClassifier
from py_pdf_term._common.data import Term


class EnglishNumericFilter(BaseEnglishCandidateTermFilter):
    def __init__(self) -> None:
        self._classifier = EnglishMorphemeClassifier()

    def is_candidate(self, scoped_term: Term) -> bool:
        return not self._is_numeric_phrase(scoped_term)

    def _is_numeric_phrase(self, scoped_term: Term) -> bool:
        def is_numeric_or_meaningless(morpheme: Morpheme) -> bool:
            return morpheme.pos == "NUM" or self._classifier.is_meaningless(morpheme)

        return all(map(is_numeric_or_meaningless, scoped_term.morphemes))
