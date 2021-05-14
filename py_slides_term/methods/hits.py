from typing import Dict, Any

from .base import BaseSingleDomainRankingMethod
from .rankingdata import HITSRankingData
from .collectors import HITSRankingDataCollector
from .rankers import HITSRanker


class HITSMethod(BaseSingleDomainRankingMethod[HITSRankingData]):
    # public
    def __init__(self, threshold: float = 1e-8):
        collector = HITSRankingDataCollector()
        ranker = HITSRanker(threshold=threshold)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_json(cls, obj: Dict[str, Any]) -> HITSRankingData:
        return HITSRankingData(**obj)
