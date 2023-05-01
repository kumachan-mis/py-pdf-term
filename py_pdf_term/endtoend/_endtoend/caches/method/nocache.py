from typing import Any, Callable, Dict, List, Union

from py_pdf_term.methods import MethodTermRanking
from py_pdf_term.methods._methods.rankingdata import RankingData

from ...configs import BaseMethodLayerConfig
from .base import BaseMethodLayerDataCache, BaseMethodLayerRankingCache


class MethodLayerRankingNoCache(BaseMethodLayerRankingCache):
    """A method layer ranking cache that does not store and load term rankings.

    Args
    ----
        cache_dir:
            This argument is ignored.
    """

    def __init__(self, cache_dir: str) -> None:
        pass

    def load(
        self,
        pdf_paths: List[str],
        config: BaseMethodLayerConfig,
    ) -> Union[MethodTermRanking, None]:
        pass

    def store(
        self,
        pdf_paths: List[str],
        term_ranking: MethodTermRanking,
        config: BaseMethodLayerConfig,
    ) -> None:
        pass

    def remove(self, pdf_paths: List[str], config: BaseMethodLayerConfig) -> None:
        pass


class MethodLayerDataNoCache(BaseMethodLayerDataCache[RankingData]):
    """A method layer data cache that does not store and load metadata to generate term
    rankings.

    Args
    ----
        cache_dir:
            This argument is ignored.
    """

    def __init__(self, cache_dir: str) -> None:
        pass

    def load(
        self,
        pdf_paths: List[str],
        config: BaseMethodLayerConfig,
        from_dict: Callable[[Dict[str, Any]], RankingData],
    ) -> Union[RankingData, None]:
        pass

    def store(
        self,
        pdf_paths: List[str],
        ranking_data: RankingData,
        config: BaseMethodLayerConfig,
    ) -> None:
        pass

    def remove(self, pdf_paths: List[str], config: BaseMethodLayerConfig) -> None:
        pass
