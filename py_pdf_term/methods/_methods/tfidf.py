from typing import Any, Dict, Literal

from .base import BaseMultiDomainRankingMethod
from .collectors import TFIDFRankingDataCollector
from .rankers import TFIDFRanker
from .rankingdata import TFIDFRankingData


class TFIDFMethod(BaseMultiDomainRankingMethod[TFIDFRankingData]):
    """A ranking method by TF-IDF algorithm.

    Args
    ----
        tfmode:
            A mode to calculate TF score. The default is `log`, which means that the
            logarithm of the term frequency is used.
        idfmode:
            A mode to calculate IDF score. The default is `natural`, which means that
            the natural logarithm of the inverse document frequency is used.
    """

    def __init__(
        self,
        tfmode: Literal["natural", "log", "augmented", "logave", "binary"] = "log",
        idfmode: Literal["natural", "smooth", "prob", "unary"] = "natural",
    ) -> None:
        collector = TFIDFRankingDataCollector()
        ranker = TFIDFRanker(tfmode=tfmode, idfmode=idfmode)
        super().__init__(collector, ranker)

    @classmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> TFIDFRankingData:
        return TFIDFRankingData(**obj)
