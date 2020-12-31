from pdf_slides_term.methods.base import BaseSingleDomainRankingMethod
from pdf_slides_term.methods.rankingdata.flr import FLRRakingData
from pdf_slides_term.methods.collectors.flr import FLRRankingDataCollector
from pdf_slides_term.methods.rankers.flr import FLRRanker


class FLRMethod(BaseSingleDomainRankingMethod[FLRRakingData]):
    # public
    def __init__(self, consider_charfont: bool = True):
        collector = FLRRankingDataCollector(collect_charfont=consider_charfont)
        ranker = FLRRanker()
        super().__init__(collector, ranker)
