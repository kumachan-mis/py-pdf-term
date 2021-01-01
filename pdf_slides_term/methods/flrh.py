from .base import BaseSingleDomainRankingMethod
from .rankingdata import FLRHRankingData
from .collectors import FLRHRankingDataCollector
from .rankers import FLRHRanker


class FLRHMethod(BaseSingleDomainRankingMethod[FLRHRankingData]):
    # public
    def __init__(self, threshold: float = 1e-8, consider_charfont: bool = True):
        collector = FLRHRankingDataCollector(collect_charfont=consider_charfont)
        ranker = FLRHRanker(threshold=threshold)
        super().__init__(collector, ranker)
