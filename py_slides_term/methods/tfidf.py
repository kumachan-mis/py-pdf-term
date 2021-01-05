from typing import Dict, Any, Literal

from .base import BaseMultiDomainRankingMethod
from .rankingdata import TFIDFRankingData
from .collectors import TFIDFRankingDataCollector
from .rankers import TFIDFRanker


class TFIDFMethod(BaseMultiDomainRankingMethod[TFIDFRankingData]):
    # public
    def __init__(
        self,
        tfmode: Literal["natural", "log", "augmented", "logave", "binary"] = "log",
        idfmode: Literal["natural", "smooth", "prob", "unary"] = "natural",
        consider_charfont: bool = True,
    ):
        collector = TFIDFRankingDataCollector(collect_charfont=consider_charfont)
        ranker = TFIDFRanker(tfmode=tfmode, idfmode=idfmode)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_json(cls, obj: Dict[str, Any]) -> TFIDFRankingData:
        return TFIDFRankingData(**obj)
