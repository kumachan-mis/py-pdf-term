from typing import Dict, Any

from .base import BaseSingleDomainRankingMethod
from .rankingdata import MCValueRankingData
from .collectors import MCValueRankingDataCollector
from .rankers import MCValueRanker


class MCValueMethod(BaseSingleDomainRankingMethod[MCValueRankingData]):
    def __init__(self) -> None:
        collector = MCValueRankingDataCollector()
        ranker = MCValueRanker()
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> MCValueRankingData:
        return MCValueRankingData(**obj)
