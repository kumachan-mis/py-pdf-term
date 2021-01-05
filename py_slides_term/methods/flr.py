from typing import Dict, Any

from .base import BaseSingleDomainRankingMethod
from .rankingdata import FLRRankingData
from .collectors import FLRRankingDataCollector
from .rankers import FLRRanker


class FLRMethod(BaseSingleDomainRankingMethod[FLRRankingData]):
    # public
    def __init__(self, consider_charfont: bool = True):
        collector = FLRRankingDataCollector(collect_charfont=consider_charfont)
        ranker = FLRRanker()
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_json(cls, obj: Dict[str, Any]) -> FLRRankingData:
        return FLRRankingData(**obj)
