from abc import ABCMeta, abstractmethod
from typing import Generic, List

from py_pdf_term.candidates import DomainCandidateTermList

from ..data import MethodTermRanking
from ..rankingdata.base import RankingData


class BaseSingleDomainRanker(Generic[RankingData], metaclass=ABCMeta):
    """Base class for term rankers with an algorithm which does not require cross-domain
    information.
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data: RankingData,
    ) -> MethodTermRanking:
        """Rank candidate terms in domain-specific PDF documents.

        Args
        ----
            domain_candidates:
                A list of candidate terms in domain-specific PDF documents.
            ranking_data:
                Metadata to rank candidate terms in PDF documents.

        Returns
        -------
            MethodTermRanking:
                A ranking result of candidate terms in PDF documents.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.rank_terms()")


class BaseMultiDomainRanker(Generic[RankingData], metaclass=ABCMeta):
    """Base class for term rankers with an algorithm which requires cross-domain
    information.
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data_list: List[RankingData],
    ) -> MethodTermRanking:
        """Rank candidate terms in domain-specific PDF documents.

        Args
        ----
            domain_candidates:
                A list of candidate terms in domain-specific PDF documents.
            ranking_data_list:
                List of metadata to rank candidate terms in PDF documents for each
                domain.

        Returns
        -------
            MethodTermRanking:
                A ranking result of candidate terms in PDF documents.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.rank_terms()")
