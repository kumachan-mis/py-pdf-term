from abc import ABCMeta, abstractmethod
from typing import List, Generic

from ..rankingdata.base import RankingData
from ..data import MethodTermRanking
from py_slides_term.candidates import DomainCandidateTermList


class BaseSingleDomainRanker(Generic[RankingData], metaclass=ABCMeta):
    # public
    def __init__(self):
        pass

    @abstractmethod
    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data: RankingData,
    ) -> MethodTermRanking:
        raise NotImplementedError(f"{self.__class__.__name__}.rank_terms()")


class BaseMultiDomainRanker(Generic[RankingData], metaclass=ABCMeta):
    # public
    def __init__(self):
        pass

    @abstractmethod
    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data_list: List[RankingData],
    ) -> MethodTermRanking:
        raise NotImplementedError(f"{self.__class__.__name__}.rank_terms()")
