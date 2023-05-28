from typing import Any

from .base import BaseSingleDomainRankingMethod
from .collectors import MCValueRankingDataCollector
from .rankers import MCValueRanker
from .rankingdata import MCValueRankingData


class MCValueMethod(BaseSingleDomainRankingMethod[MCValueRankingData]):
    """Ranking method by MC-Value algorithm."""

    def __init__(self) -> None:
        collector = MCValueRankingDataCollector()
        ranker = MCValueRanker()
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: dict[str, Any]) -> MCValueRankingData:
        return MCValueRankingData(**obj)
