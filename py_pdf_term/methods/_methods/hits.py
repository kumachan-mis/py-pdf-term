from typing import Any

from .base import BaseSingleDomainRankingMethod
from .collectors import HITSRankingDataCollector
from .rankers import HITSRanker
from .rankingdata import HITSRankingData


class HITSMethod(BaseSingleDomainRankingMethod[HITSRankingData]):
    """Ranking method by HITS algorithm.

    Args
    ----
        threshold:
            Threshold to determine convergence. If the difference between
            original auth/hub values and new auth/hub values is less than this
            threshold, the algorithm is considered to be converged. The default is 1e-8.
        max_loop:
            Maximum number of loops to run the algorithm. If the algorithm
            does not converge within this number of loops, it is forced to stop. The
            default is 1000.
    """

    def __init__(self, threshold: float = 1e-8, max_loop: int = 1000) -> None:
        collector = HITSRankingDataCollector()
        ranker = HITSRanker(threshold=threshold, max_loop=max_loop)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: dict[str, Any]) -> HITSRankingData:
        return HITSRankingData(**obj)
