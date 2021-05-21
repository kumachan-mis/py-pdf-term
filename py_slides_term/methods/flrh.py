from typing import Dict, Any

from .base import BaseSingleDomainRankingMethod
from .rankingdata import FLRHRankingData
from .collectors import FLRHRankingDataCollector
from .rankers import FLRHRanker


class FLRHMethod(BaseSingleDomainRankingMethod[FLRHRankingData]):
    # public
    def __init__(self, threshold: float = 1e-8):
        collector = FLRHRankingDataCollector()
        ranker = FLRHRanker(threshold=threshold)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> FLRHRankingData:
        return FLRHRankingData(**obj)
