from typing import Any, Dict, Literal

from .base import BaseMultiDomainRankingMethod
from .collectors import TFIDFRankingDataCollector
from .rankers import TFIDFRanker
from .rankingdata import TFIDFRankingData


class TFIDFMethod(BaseMultiDomainRankingMethod[TFIDFRankingData]):
    def __init__(
        self,
        tfmode: Literal["natural", "log", "augmented", "logave", "binary"] = "log",
        idfmode: Literal["natural", "smooth", "prob", "unary"] = "natural",
    ) -> None:
        collector = TFIDFRankingDataCollector()
        ranker = TFIDFRanker(tfmode=tfmode, idfmode=idfmode)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> TFIDFRankingData:
        return TFIDFRankingData(**obj)
