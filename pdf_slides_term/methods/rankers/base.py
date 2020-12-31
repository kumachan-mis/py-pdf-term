from abc import ABCMeta, abstractmethod
from typing import List, Generic

from pdf_slides_term.methods.rankingdata.base import RankingData
from pdf_slides_term.methods.data import DomainTermRanking
from pdf_slides_term.candidates.data import DomainCandidateTermList


class BaseSingleDomainRanker(Generic[RankingData], metaclass=ABCMeta):
    # public
    def __init__(self):
        pass

    @abstractmethod
    def rank_terms(
        self, domain_candidates: DomainCandidateTermList, ranking_data: RankingData
    ) -> DomainTermRanking:
        raise NotImplementedError(
            f"{self.__class__.__name__}.rank_terms() is not implemented"
        )


class BaseMultiDomainRanker(Generic[RankingData], metaclass=ABCMeta):
    # public
    def __init__(self):
        pass

    @abstractmethod
    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data: RankingData,
        other_ranking_data_list: List[RankingData],
    ) -> DomainTermRanking:
        raise NotImplementedError(
            f"{self.__class__.__name__}.rank_terms() is not implemented"
        )