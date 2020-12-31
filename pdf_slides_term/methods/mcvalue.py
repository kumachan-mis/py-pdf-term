from pdf_slides_term.methods.base import BaseSingleDomainRankingMethod
from pdf_slides_term.methods.rankingdata.mcvalue import MCValueRakingData
from pdf_slides_term.methods.collectors.mcvalue import MCValueRankingDataCollector
from pdf_slides_term.methods.rankers.mcvalue import MCValueRanker


class MCValueMethod(BaseSingleDomainRankingMethod[MCValueRakingData]):
    # public
    def __init__(self, consider_charfont: bool = True):
        collector = MCValueRankingDataCollector(collect_charfont=consider_charfont)
        ranker = MCValueRanker()
        super().__init__(collector, ranker)
