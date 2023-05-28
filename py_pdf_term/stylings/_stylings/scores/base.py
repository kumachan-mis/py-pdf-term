from abc import ABCMeta, abstractmethod

from py_pdf_term.candidates import PageCandidateTermList
from py_pdf_term.tokenizers import Term


class BaseStylingScore(metaclass=ABCMeta):
    """Base class for styling scores. A styling score is expected to focus on a single
    styling feature, such as font size, font family, and font color. The score is
    calculated per a page of a PDF file, not per a domain of PDF files.

    Args
    ----
        page_candidates:
            List of candidate terms in a page of a PDF file. The target of analysis.
    """

    def __init__(self, page_candidates: PageCandidateTermList) -> None:
        pass

    @abstractmethod
    def calculate_score(self, candidate: Term) -> float:
        """Calculate the styling score of a candidate term.

        Args
        ----
            candidate:
                Candidate term to calculate the styling score. This term is expected
                to be included in the list of candidate terms passed to the constructor.

        Returns
        -------
            float:
                The styling score of the candidate term.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.calculate_score()")
