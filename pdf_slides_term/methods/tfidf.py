from typing import Literal

from pdf_slides_term.methods.base import BaseMultiDomainRankingMethod
from pdf_slides_term.methods.rankingdata.tfidf import TFIDFRankingData
from pdf_slides_term.methods.collectors.tfidf import TFIDFRankingDataCollector
from pdf_slides_term.methods.rankers.tfidf import TFIDFRanker


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
