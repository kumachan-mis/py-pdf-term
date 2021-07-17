from ..base import BaseJapaneseCandidateTermFilter
from py_pdf_term.tokenizer import Morpheme
from py_pdf_term.tokenizer.langs import JapaneseMorphemeClassifier
from py_pdf_term._common.data import Term


class JapaneseNumericFilter(BaseJapaneseCandidateTermFilter):
    def __init__(self) -> None:
        self._classifier = JapaneseMorphemeClassifier()

    def is_candidate(self, scoped_term: Term) -> bool:
        return not self._is_numeric_phrase(scoped_term)

    def _is_numeric_phrase(self, scoped_term: Term) -> bool:
        def is_numeric_or_meaningless(morpheme: Morpheme) -> bool:
            return (
                morpheme.pos == "接頭辞"
                or (morpheme.pos == "名詞" and morpheme.category == "数詞")
                or (
                    morpheme.pos == "名詞"
                    and morpheme.category == "普通名詞"
                    and morpheme.subcategory == "助数詞可能"
                )
                or morpheme.pos == "接尾辞"
                or self._classifier.is_meaningless(morpheme)
            )

        return all(map(is_numeric_or_meaningless, scoped_term.morphemes))
