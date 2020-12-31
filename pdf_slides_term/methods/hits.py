from pdf_slides_term.methods.base import BaseSingleDomainRankingMethod
from pdf_slides_term.methods.rankingdata.hits import HITSRakingData
from pdf_slides_term.methods.collectors.hits import HITSRankingDataCollector
from pdf_slides_term.methods.rankers.hits import HITSRanker


class HITSMethod(BaseSingleDomainRankingMethod[HITSRakingData]):
    # public
    def __init__(self, consider_charfont: bool = True):
        collector = HITSRankingDataCollector(collect_charfont=consider_charfont)
        ranker = HITSRanker()
        super().__init__(collector, ranker)
