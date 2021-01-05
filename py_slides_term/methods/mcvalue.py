from typing import Dict, Any

from .base import BaseSingleDomainRankingMethod
from .rankingdata import MCValueRankingData
from .collectors import MCValueRankingDataCollector
from .rankers import MCValueRanker


class MCValueMethod(BaseSingleDomainRankingMethod[MCValueRankingData]):
    # public
    def __init__(self, consider_charfont: bool = True):
        collector = MCValueRankingDataCollector(collect_charfont=consider_charfont)
        ranker = MCValueRanker()
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_json(cls, obj: Dict[str, Any]) -> MCValueRankingData:
        return MCValueRankingData(**obj)
