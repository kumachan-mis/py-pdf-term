from typing import Literal

from pdf_slides_term.methods.base import BaseMultiDomainRankingMethod
from pdf_slides_term.methods.rankingdata.lfidf import LFIDFRankingData
from pdf_slides_term.methods.collectors.lfidf import LFIDFRankingDataCollector
from pdf_slides_term.methods.rankers.lfidf import LFIDFRanker


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
