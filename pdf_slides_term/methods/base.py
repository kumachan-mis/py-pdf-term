from abc import ABCMeta, abstractmethod
from typing import List

from pdf_slides_term.methods.data import DomainTermRanking
from pdf_slides_term.candidates.data import DomainCandidateTermList


class BaseSingleDomainTermRankingMethod(metaclass=ABCMeta):
    # public
    @abstractmethod
    def rank_terms(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainTermRanking:
        raise NotImplementedError(
            f"{self.__class__.__name__}.extract() is not implemented"
        )


class BaseMultipleDomainTermRankingMethod(metaclass=ABCMeta):
    # public
    @abstractmethod
    def rank_terms(
        self, domain: str, domain_candidates: List[DomainCandidateTermList]
    ) -> DomainTermRanking:
        raise NotImplementedError(
            f"{self.__class__.__name__}.extract() is not implemented"
        )
