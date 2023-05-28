from math import exp
from statistics import mean, stdev

from py_pdf_term.candidates import PageCandidateTermList
from py_pdf_term.tokenizers import Term

from .base import BaseStylingScore


class FontsizeScore(BaseStylingScore):
    """Styling score for font size. The larger the font size is, the higher the score
    is. The score is normalized by the mean and the standard deviation of font sizes in
    the page.

    Args:
        page_candidates:
            List of candidate terms in a page of a PDF file. The target of analysis.
    """

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
