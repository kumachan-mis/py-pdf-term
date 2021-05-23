from typing import Dict, Any, Literal

from .base import BaseMultiDomainRankingMethod
from .rankingdata import LFIDFRankingData
from .collectors import LFIDFRankingDataCollector
from .rankers import LFIDFRanker


class LFIDFMethod(BaseMultiDomainRankingMethod[LFIDFRankingData]):
    def __init__(
        self,
        lfmode: Literal["natural", "log", "augmented", "logave", "binary"] = "log",
        idfmode: Literal["natural", "smooth", "prob", "unary"] = "natural",
    ) -> None:
        collector = LFIDFRankingDataCollector()
        ranker = LFIDFRanker(lfmode=lfmode, idfmode=idfmode)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> LFIDFRankingData:
        return LFIDFRankingData(**obj)
