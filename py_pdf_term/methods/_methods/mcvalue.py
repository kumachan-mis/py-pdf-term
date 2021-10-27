from typing import Any, Dict

from .base import BaseSingleDomainRankingMethod
from .collectors import MCValueRankingDataCollector
from .rankers import MCValueRanker
from .rankingdata import MCValueRankingData


class MCValueMethod(BaseSingleDomainRankingMethod[MCValueRankingData]):
    def __init__(self) -> None:
        collector = MCValueRankingDataCollector()
        ranker = MCValueRanker()
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> MCValueRankingData:
        return MCValueRankingData(**obj)
