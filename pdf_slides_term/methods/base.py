from abc import ABCMeta
from typing import List, Iterator, Generic

from .collectors import BaseRankingDataCollector
from .rankers import BaseSingleDomainRanker, BaseMultiDomainRanker
from .data import DomainTermRanking
from .rankingdata.base import RankingData
from pdf_slides_term.candidates import DomainCandidateTermList


class BaseSingleDomainRankingMethod(Generic[RankingData], metaclass=ABCMeta):
    # public
    def __init__(
        self,
        data_collector: BaseRankingDataCollector[RankingData],
        ranker: BaseSingleDomainRanker[RankingData],
    ):
        self.data_collector = data_collector
        self._ranker = ranker

    def rank_terms(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainTermRanking:
        ranking_data = self.data_collector.collect(domain_candidates)
        domain_term_ranking = self._ranker.rank_terms(domain_candidates, ranking_data)
        return domain_term_ranking


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
        self, domain_candidates_list: List[DomainCandidateTermList]
    ) -> Iterator[DomainTermRanking]:
        ranking_data_list = list(
            map(self._data_collector.collect, domain_candidates_list)
        )

        for domain_candidates in domain_candidates_list:
            ranking_data = next(
                filter(
                    lambda item: item.domain == domain_candidates.domain,
                    ranking_data_list,
                ),
            )
            other_ranking_data_list = list(
                filter(
                    lambda item: item.domain != domain_candidates.domain,
                    ranking_data_list,
                )
            )
            domain_term_ranking = self._ranker.rank_terms(
                domain_candidates, ranking_data, other_ranking_data_list
            )
            yield domain_term_ranking

    def rank_domain_terms(
        self, domain: str, domain_candidates_list: List[DomainCandidateTermList]
    ) -> DomainTermRanking:
        domain_candidates = next(
            filter(lambda item: item.domain == domain, domain_candidates_list),
            None,
        )
        other_domain_candidates_list = list(
            filter(lambda item: item.domain != domain, domain_candidates_list)
        )

        if domain_candidates is None:
            raise ValueError(f"candidate term list in '{domain}' is not provided")

        ranking_data = self._data_collector.collect(domain_candidates)
        other_ranking_data_list = list(
            map(self._data_collector.collect, other_domain_candidates_list)
        )

        domain_term_ranking = self._ranker.rank_terms(
            domain_candidates, ranking_data, other_ranking_data_list
        )
        return domain_term_ranking
