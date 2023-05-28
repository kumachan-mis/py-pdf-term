from typing import Any

from .base import BaseSingleDomainRankingMethod
from .collectors import FLRRankingDataCollector
from .rankers import FLRRanker
from .rankingdata import FLRRankingData


class FLRMethod(BaseSingleDomainRankingMethod[FLRRankingData]):
    """Ranking method by FLR algorithm."""

    def __init__(self) -> None:
        collector = FLRRankingDataCollector()
        ranker = FLRRanker()
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: dict[str, Any]) -> FLRRankingData:
        return FLRRankingData(**obj)
