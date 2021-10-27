from abc import ABCMeta, abstractmethod

from py_pdf_term._common.data import Term
from py_pdf_term.candidates import PageCandidateTermList


class BaseStylingScore(metaclass=ABCMeta):
    def __init__(self, page_candidates: PageCandidateTermList) -> None:
        pass

    @abstractmethod
    def calculate_score(self, candidate: Term) -> float:
        raise NotImplementedError(f"{self.__class__.__name__}.calculate_score()")
