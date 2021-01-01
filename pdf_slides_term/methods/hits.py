from .base import BaseSingleDomainRankingMethod
from .rankingdata import HITSRankingData
from .collectors import HITSRankingDataCollector
from .rankers import HITSRanker


class HITSMethod(BaseSingleDomainRankingMethod[HITSRankingData]):
    # public
    def __init__(self, threshold: float = 1e-8, consider_charfont: bool = True):
        collector = HITSRankingDataCollector(collect_charfont=consider_charfont)
        ranker = HITSRanker(threshold=threshold)
        super().__init__(collector, ranker)
