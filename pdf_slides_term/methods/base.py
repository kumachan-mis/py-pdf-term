from abc import ABCMeta, abstractmethod
from typing import List, Iterator

from pdf_slides_term.methods.data import DomainTermRanking
from pdf_slides_term.candidates.data import DomainCandidateTermList


class BaseSingleDomainTermRankingMethod(metaclass=ABCMeta):
    # public
    @abstractmethod
    def rank_terms(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainTermRanking:
        raise NotImplementedError(
            f"{self.__class__.__name__}.rank_terms() is not implemented"
        )


class BaseMultipleDomainTermRankingMethod(metaclass=ABCMeta):
    # public
    @abstractmethod
    def rank_terms(
        self, domain_candidates_list: List[DomainCandidateTermList]
    ) -> Iterator[DomainTermRanking]:
        raise NotImplementedError(
            f"{self.__class__.__name__}.rank_terms() is not implemented"
        )

    @abstractmethod
    def rank_domain_terms(
        self, domain: str, domain_candidates_list: List[DomainCandidateTermList]
    ) -> DomainTermRanking:
        raise NotImplementedError(
            f"{self.__class__.__name__}.rank_domain_terms() is not implemented"
        )
