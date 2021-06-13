from typing import Dict, Any

from .base import BaseSingleDomainRankingMethod
from .rankingdata import HITSRankingData
from .collectors import HITSRankingDataCollector
from .rankers import HITSRanker


class HITSMethod(BaseSingleDomainRankingMethod[HITSRankingData]):
    def __init__(self, threshold: float = 1e-8, max_loop: int = 1000) -> None:
        collector = HITSRankingDataCollector()
        ranker = HITSRanker(threshold=threshold, max_loop=max_loop)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> HITSRankingData:
        return HITSRankingData(**obj)
