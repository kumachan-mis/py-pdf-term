from typing import Literal

from .base import BaseMultiDomainRankingMethod
from .rankingdata import LFIDFRankingData
from .collectors import LFIDFRankingDataCollector
from .rankers import LFIDFRanker


class LFIDFMethod(BaseMultiDomainRankingMethod[LFIDFRankingData]):
    # public
    def __init__(
        self,
        tfmode: Literal["natural", "log", "augmented", "logave", "binary"] = "log",
        idfmode: Literal["natural", "smooth", "prob", "unary"] = "natural",
        consider_charfont: bool = True,
    ):
        collector = LFIDFRankingDataCollector(collect_charfont=consider_charfont)
        ranker = LFIDFRanker(tfmode=tfmode, idfmode=idfmode)
        super().__init__(collector, ranker)
