from typing import List

from .morpheme import BaseCandidateMorphemeFilter
from .term import BaseCandidateTermFilter
from py_slides_term.morphemes import BaseMorpheme
from py_slides_term.share.data import Term


class CandidateFilter:
    # public

    def __init__(
        self,
        morpheme_filters: List[BaseCandidateMorphemeFilter],
        term_filters: List[BaseCandidateTermFilter],
    ):
        self._morpheme_filters = morpheme_filters
        self._term_filters = term_filters

    def is_partof_candidate(self, morphemes: List[BaseMorpheme], idx: int) -> bool:
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
