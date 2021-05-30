from typing import Dict, Any

from .base import BaseSingleDomainRankingMethod
from .rankingdata import FLRRankingData
from .collectors import FLRRankingDataCollector
from .rankers import FLRRanker


class FLRMethod(BaseSingleDomainRankingMethod[FLRRankingData]):
    def __init__(self) -> None:
        collector = FLRRankingDataCollector()
        ranker = FLRRanker()
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> FLRRankingData:
        return FLRRankingData(**obj)
