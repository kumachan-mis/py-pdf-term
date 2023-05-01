from typing import Any, Callable, Dict, Iterable

from .base import BaseMultiDomainRankingMethod
from .collectors import MDPRankingDataCollector
from .rankers import MDPRanker
from .rankingdata import MDPRankingData


class MDPMethod(BaseMultiDomainRankingMethod[MDPRankingData]):
    """A ranking method by MDP algorithm.

    Args
    ----
        compile_scores:
            A function to compile scores of candidate terms in each domain.
            The default is `min`, which means that the minimum score is used.
    """

    def __init__(
        self, compile_scores: Callable[[Iterable[float]], float] = min
    ) -> None:
        collector = MDPRankingDataCollector()
        ranker = MDPRanker(compile_scores=compile_scores)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> MDPRankingData:
        return MDPRankingData(**obj)
