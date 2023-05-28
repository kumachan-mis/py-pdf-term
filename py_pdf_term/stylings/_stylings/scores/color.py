from py_pdf_term._common.utils import extended_log10
from py_pdf_term.candidates import PageCandidateTermList
from py_pdf_term.tokenizers import Term

from .base import BaseStylingScore


class ColorScore(BaseStylingScore):
    """Styling score for font color. The more rarely the color appears in the page,
    the higher the score is.

    Args
    ----
        page_candidates:
            List of candidate terms in a page of a PDF file. The target of analysis.
    """

    def __init__(self, page_candidates: PageCandidateTermList) -> None:
        super().__init__(page_candidates)

        self._num_candidates = len(page_candidates.candidates)

        self._color_freq: dict[str, int] = dict()
        for candidate in page_candidates.candidates:
            self._color_freq[candidate.ncolor] = (
                self._color_freq.get(candidate.ncolor, 0) + 1
            )

    def calculate_score(self, candidate: Term) -> float:
        if self._num_candidates == 0 or candidate.ncolor not in self._color_freq:
            return 1.0

        ncolor_prob = self._color_freq.get(candidate.ncolor, 0) / self._num_candidates
        return -extended_log10(ncolor_prob) + 1.0
