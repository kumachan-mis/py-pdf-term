from math import exp
from statistics import mean, stdev

from py_pdf_term._common.data import Term
from py_pdf_term.candidates import PageCandidateTermList

from .base import BaseStylingScore


class FontsizeScore(BaseStylingScore):
    def __init__(self, page_candidates: PageCandidateTermList) -> None:
        super().__init__(page_candidates)

        self._num_candidates = len(page_candidates.candidates)

        self._fontsize_mean = (
            mean(map(lambda candidate: candidate.fontsize, page_candidates.candidates))
            if self._num_candidates >= 1
            else None
        )
        self._fontsize_stdev = (
            stdev(
                map(lambda candidate: candidate.fontsize, page_candidates.candidates),
                self._fontsize_mean,
            )
            if self._num_candidates >= 2
            else None
        )

    def calculate_score(self, candidate: Term) -> float:
        if self._fontsize_mean is None or self._fontsize_stdev is None:
            return 1.0
        if self._fontsize_stdev == 0:
            return 1.0

        z = (candidate.fontsize - self._fontsize_mean) / self._fontsize_stdev
        return 2 / (1 + exp(-z))
