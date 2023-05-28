from typing import Any

from .base import BaseMultiDomainRankingMethod
from .collectors import TFIDFRankingDataCollector
from .rankers import TFIDFRanker
from .rankingdata import TFIDFRankingData


class TFIDFMethod(BaseMultiDomainRankingMethod[TFIDFRankingData]):
    """Ranking method by TF-IDF algorithm."""

    def __init__(self) -> None:
        collector = TFIDFRankingDataCollector()
        ranker = TFIDFRanker()
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: dict[str, Any]) -> TFIDFRankingData:
        return TFIDFRankingData(**obj)
