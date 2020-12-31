from pdf_slides_term.methods.base import BaseMultiDomainRankingMethod
from pdf_slides_term.methods.rankingdata.tfidf import TFIDFRankingData
from pdf_slides_term.methods.collectors.tfidf import TFIDFRankingDataCollector
from pdf_slides_term.methods.rankers.tfidf import TFIDFRanker


class MDPMethod(BaseMultiDomainRankingMethod[TFIDFRankingData]):
    # public
    def __init__(self, consider_charfont: bool = True):
        collector = TFIDFRankingDataCollector(collect_charfont=consider_charfont)
        ranker = TFIDFRanker()
        super().__init__(collector, ranker)
