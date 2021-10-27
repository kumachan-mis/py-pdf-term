from typing import Any, Callable, Dict, Iterable

from .base import BaseMultiDomainRankingMethod
from .collectors import MDPRankingDataCollector
from .rankers import MDPRanker
from .rankingdata import MDPRankingData


class MDPMethod(BaseMultiDomainRankingMethod[MDPRankingData]):
    def __init__(
        self, compile_scores: Callable[[Iterable[float]], float] = min
    ) -> None:
        collector = MDPRankingDataCollector()
        ranker = MDPRanker(compile_scores=compile_scores)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> MDPRankingData:
        return MDPRankingData(**obj)
