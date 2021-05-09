from typing import List, Dict, Any, Union, Callable, Generic

from .base import BaseMethodLayerRankingCache, BaseMethodLayerDataCache
from ...configs import MethodLayerConfig
from py_slides_term.methods import DomainTermRanking
from py_slides_term.methods.rankingdata import RankingData


class MethodLayerRankingNoCache(BaseMethodLayerRankingCache):
    # public
    def __init__(self, cache_dirlike: str):
        pass

    def load(
        self,
        pdf_paths: List[str],
        config: MethodLayerConfig,
    ) -> Union[DomainTermRanking, None]:
        pass

    def store(
        self,
        pdf_paths: List[str],
        term_ranking: DomainTermRanking,
        config: MethodLayerConfig,
    ) -> None:
        pass

    def remove(self, pdf_paths: List[str], config: MethodLayerConfig) -> None:
        pass


class MethodLayerDataNoCache(
    Generic[RankingData], BaseMethodLayerDataCache[RankingData]
):
    # public
    def __init__(self, cache_dirlike: str):
        pass

    def load(
        self,
        pdf_paths: List[str],
        config: MethodLayerConfig,
        from_json: Callable[[Dict[str, Any]], RankingData],
    ) -> Union[RankingData, None]:
        pass

    def store(
        self,
        pdf_paths: List[str],
        ranking_data: RankingData,
        config: MethodLayerConfig,
    ) -> None:
        pass

    def remove(self, pdf_paths: List[str], config: MethodLayerConfig) -> None:
        pass
