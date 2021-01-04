from abc import ABCMeta
from typing import Generic

from ..collectors import BaseRankingDataCollector
from ..rankers import BaseSingleDomainRanker
from ..data import DomainTermRanking
from ..rankingdata.base import RankingData
from py_slides_term.candidates import DomainCandidateTermList


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
