from typing import Any, Dict

from .base import BaseSingleDomainRankingMethod
from .collectors import FLRRankingDataCollector
from .rankers import FLRRanker
from .rankingdata import FLRRankingData


class FLRMethod(BaseSingleDomainRankingMethod[FLRRankingData]):
    def __init__(self) -> None:
        collector = FLRRankingDataCollector()
        ranker = FLRRanker()
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> FLRRankingData:
        return FLRRankingData(**obj)
