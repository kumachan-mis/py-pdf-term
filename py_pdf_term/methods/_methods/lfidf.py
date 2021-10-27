from typing import Any, Dict

from .base import BaseMultiDomainRankingMethod
from .collectors import LFIDFRankingDataCollector
from .rankers import LFIDFRanker
from .rankingdata import LFIDFRankingData


class LFIDFMethod(BaseMultiDomainRankingMethod[LFIDFRankingData]):
    def __init__(self, lfmode: str = "log", idfmode: str = "natural") -> None:
        collector = LFIDFRankingDataCollector()
        ranker = LFIDFRanker(lfmode=lfmode, idfmode=idfmode)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> LFIDFRankingData:
        return LFIDFRankingData(**obj)
