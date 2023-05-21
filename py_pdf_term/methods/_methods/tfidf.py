from typing import Any, Dict

from .base import BaseMultiDomainRankingMethod
from .collectors import TFIDFRankingDataCollector
from .rankers import TFIDFRanker
from .rankingdata import TFIDFRankingData


class TFIDFMethod(BaseMultiDomainRankingMethod[TFIDFRankingData]):
    """A ranking method by TF-IDF algorithm."""

    def __init__(self) -> None:
        collector = TFIDFRankingDataCollector()
        ranker = TFIDFRanker()
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> TFIDFRankingData:
        return TFIDFRankingData(**obj)
