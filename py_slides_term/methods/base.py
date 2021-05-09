from abc import ABCMeta, abstractmethod
from typing import List, Dict, Any, Generic, Iterator, Optional

from .collectors import BaseRankingDataCollector
from .rankers import BaseSingleDomainRanker, BaseMultiDomainRanker
from .data import DomainTermRanking
from .rankingdata.base import RankingData
from py_slides_term.candidates import DomainCandidateTermList


class BaseSingleDomainRankingMethod(Generic[RankingData], metaclass=ABCMeta):
    # public
    def __init__(
        self,
        data_collector: BaseRankingDataCollector[RankingData],
        ranker: BaseSingleDomainRanker[RankingData],
    ):
        self._data_collector = data_collector
        self._ranker = ranker

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data: Optional[RankingData] = None,
    ) -> DomainTermRanking:
        if ranking_data is None:
            ranking_data = self._data_collector.collect(domain_candidates)
        domain_term_ranking = self._ranker.rank_terms(domain_candidates, ranking_data)
        return domain_term_ranking

    def collect_data(self, domain_candidates: DomainCandidateTermList) -> RankingData:
        ranking_data = self._data_collector.collect(domain_candidates)
        return ranking_data

    @classmethod
    @abstractmethod
    def collect_data_from_json(cls, obj: Dict[str, Any]) -> RankingData:
        raise NotImplementedError(f"{cls.__name__}.collect_data_from_json()")


class BaseMultiDomainRankingMethod(Generic[RankingData], metaclass=ABCMeta):
    # public
    def __init__(
        self,
        data_collector: BaseRankingDataCollector[RankingData],
        ranker: BaseMultiDomainRanker[RankingData],
    ):
        self._data_collector = data_collector
        self._ranker = ranker

    def rank_terms(
        self,
        domain_candidates_list: List[DomainCandidateTermList],
        ranking_data_list: Optional[List[RankingData]] = None,
    ) -> Iterator[DomainTermRanking]:
        if ranking_data_list is None:
            ranking_data_list = list(
                map(self._data_collector.collect, domain_candidates_list)
            )

        for domain_candidates in domain_candidates_list:
            domain_term_ranking = self._ranker.rank_terms(
                domain_candidates, ranking_data_list
            )
            yield domain_term_ranking

    def rank_domain_terms(
        self,
        domain: str,
        domain_candidates_list: List[DomainCandidateTermList],
        ranking_data_list: Optional[List[RankingData]] = None,
    ) -> DomainTermRanking:
        domain_candidates = next(
            filter(lambda item: item.domain == domain, domain_candidates_list)
        )

        if ranking_data_list is None:
            ranking_data_list = list(
                map(self._data_collector.collect, domain_candidates_list)
            )

        domain_term_ranking = self._ranker.rank_terms(
            domain_candidates, ranking_data_list
        )
        return domain_term_ranking

    def collect_data(self, domain_candidates: DomainCandidateTermList) -> RankingData:
        ranking_data = self._data_collector.collect(domain_candidates)
        return ranking_data

    @classmethod
    @abstractmethod
    def collect_data_from_json(cls, obj: Dict[str, Any]) -> RankingData:
        raise NotImplementedError(f"{cls.__name__}.collect_data_from_json()")
