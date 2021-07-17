from typing import List, Optional

from .morpheme import (
    BaseCandidateMorphemeFilter,
    JapaneseMorphemeFilter,
    EnglishMorphemeFilter,
)
from .term import (
    BaseCandidateTermFilter,
    JapaneseConcatenationFilter,
    EnglishConcatenationFilter,
    JapaneseSymbolLikeFilter,
    EnglishSymbolLikeFilter,
    JapaneseProperNounFilter,
    EnglishProperNounFilter,
    JapaneseNumericFilter,
    EnglishNumericFilter,
)
from py_pdf_term.tokenizer import Morpheme
from py_pdf_term._common.data import Term


class FilterCombiner:
    def __init__(
        self,
        morpheme_filters: Optional[List[BaseCandidateMorphemeFilter]] = None,
        term_filters: Optional[List[BaseCandidateTermFilter]] = None,
    ) -> None:
        if morpheme_filters is None:
            morpheme_filters = [
                JapaneseMorphemeFilter(),
                EnglishMorphemeFilter(),
            ]
        if term_filters is None:
            term_filters = [
                JapaneseConcatenationFilter(),
                EnglishConcatenationFilter(),
                JapaneseSymbolLikeFilter(),
                EnglishSymbolLikeFilter(),
                JapaneseProperNounFilter(),
                EnglishProperNounFilter(),
                JapaneseNumericFilter(),
                EnglishNumericFilter(),
            ]

        self._morpheme_filters = morpheme_filters
        self._term_filters = term_filters

    def is_partof_candidate(self, morphemes: List[Morpheme], idx: int) -> bool:
        morpheme = morphemes[idx]
        if all(map(lambda mf: not mf.inscope(morpheme), self._morpheme_filters)):
            return False

        return all(
            map(
                lambda mf: not mf.inscope(morpheme)
                or mf.is_partof_candidate(morphemes, idx),
                self._morpheme_filters,
            )
        )

    def is_candidate(self, term: Term) -> bool:
        if all(map(lambda tf: not tf.inscope(term), self._term_filters)):
            return False

        return all(
            map(
                lambda tf: not tf.inscope(term) or tf.is_candidate(term),
                self._term_filters,
            )
        )
