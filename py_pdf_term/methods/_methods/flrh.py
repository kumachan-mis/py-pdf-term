from typing import Any, Dict

from .base import BaseSingleDomainRankingMethod
from .collectors import FLRHRankingDataCollector
from .rankers import FLRHRanker
from .rankingdata import FLRHRankingData


class FLRHMethod(BaseSingleDomainRankingMethod[FLRHRankingData]):
    def __init__(self, threshold: float = 1e-8, max_loop: int = 1000) -> None:
        collector = FLRHRankingDataCollector()
        ranker = FLRHRanker(threshold=threshold, max_loop=max_loop)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> FLRHRankingData:
        return FLRHRankingData(**obj)
