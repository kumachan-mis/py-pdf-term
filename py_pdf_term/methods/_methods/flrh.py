from typing import Any

from .base import BaseSingleDomainRankingMethod
from .collectors import FLRHRankingDataCollector
from .rankers import FLRHRanker
from .rankingdata import FLRHRankingData


class FLRHMethod(BaseSingleDomainRankingMethod[FLRHRankingData]):
    """Ranking method by FLRH algorithm. This algorithm is a combination of FLR and
    HITS.

    Args
    ----
        threshold:
            Threshold of the FLRH algorithm. The default is 1e-8.

        max_loop:
            Maximum number of loops of the FLRH algorithm. The default is 1000.
    """

    def __init__(self, threshold: float = 1e-8, max_loop: int = 1000) -> None:
        collector = FLRHRankingDataCollector()
        ranker = FLRHRanker(threshold=threshold, max_loop=max_loop)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: dict[str, Any]) -> FLRHRankingData:
        return FLRHRankingData(**obj)
