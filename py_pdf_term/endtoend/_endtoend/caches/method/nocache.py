from typing import Any, Callable

from py_pdf_term.methods import MethodTermRanking
from py_pdf_term.methods._methods.rankingdata import BaseRankingData

from ...configs import BaseMethodLayerConfig
from .base import BaseMethodLayerDataCache, BaseMethodLayerRankingCache


class MethodLayerRankingNoCache(BaseMethodLayerRankingCache):
    """Method layer ranking cache that does not store and load term rankings.

    Args
    ----
        cache_dir:
            This argument is ignored.
    """

    def __init__(self, cache_dir: str) -> None:
        pass

    def load(
        self,
        pdf_paths: list[str],
        config: BaseMethodLayerConfig,
    ) -> MethodTermRanking | None:
        pass

    def store(
        self,
        pdf_paths: list[str],
        term_ranking: MethodTermRanking,
        config: BaseMethodLayerConfig,
    ) -> None:
        pass

    def remove(self, pdf_paths: list[str], config: BaseMethodLayerConfig) -> None:
        pass


class MethodLayerDataNoCache[RankingData: BaseRankingData](
    BaseMethodLayerDataCache[RankingData]
):
    """Method layer data cache that does not store and load metadata to generate term
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
        pdf_paths: list[str],
        config: BaseMethodLayerConfig,
        from_dict: Callable[[dict[str, Any]], RankingData],
    ) -> RankingData | None:
        pass

    def store(
        self,
        pdf_paths: list[str],
        ranking_data: RankingData,
        config: BaseMethodLayerConfig,
    ) -> None:
        pass

    def remove(self, pdf_paths: list[str], config: BaseMethodLayerConfig) -> None:
        pass
