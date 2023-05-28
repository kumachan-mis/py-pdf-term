from typing import Any

from .base import BaseMultiDomainRankingMethod
from .collectors import MDPRankingDataCollector
from .rankers import MDPRanker
from .rankingdata import MDPRankingData


class MDPMethod(BaseMultiDomainRankingMethod[MDPRankingData]):
    """Ranking method by MDP algorithm."""

    def __init__(self) -> None:
        collector = MDPRankingDataCollector()
        ranker = MDPRanker()
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: dict[str, Any]) -> MDPRankingData:
        return MDPRankingData(**obj)
