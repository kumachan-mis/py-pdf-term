from typing import Dict, Any, Callable, Iterable

from .base import BaseMultiDomainRankingMethod
from .rankingdata import MDPRankingData
from .collectors import MDPRankingDataCollector
from .rankers import MDPRanker


class MDPMethod(BaseMultiDomainRankingMethod[MDPRankingData]):
    # public
    def __init__(self, compile_scores: Callable[[Iterable[float]], float] = min):
        collector = MDPRankingDataCollector()
        ranker = MDPRanker(compile_scores=compile_scores)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> MDPRankingData:
        return MDPRankingData(**obj)
