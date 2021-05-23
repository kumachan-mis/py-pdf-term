from typing import Dict

from .base import BaseStylingScore
from py_slides_term.candidates import PageCandidateTermList
from py_slides_term.share.data import Term
from py_slides_term.share.extended_math import extended_log10


class ColorScore(BaseStylingScore):
    def __init__(self, page_candidates: PageCandidateTermList):
        super().__init__(page_candidates)

        self._num_candidates = len(page_candidates.candidates)

        self._color_freq: Dict[str, int] = dict()
        for candidate in page_candidates.candidates:
            self._color_freq[candidate.ncolor] = (
                self._color_freq.get(candidate.ncolor, 0) + 1
            )

    def calculate_score(self, candidate: Term) -> float:
        if self._num_candidates == 0 or candidate.ncolor not in self._color_freq:
            return 1.0

        ncolor_prob = self._color_freq.get(candidate.ncolor, 0) / self._num_candidates
        return -extended_log10(ncolor_prob) + 1.0
