from typing import List, Dict, Any, Union, Callable

from .base import BaseMethodLayerRankingCache, BaseMethodLayerDataCache
from ...configs import MethodLayerConfig
from py_pdf_term.methods import MethodTermRanking
from py_pdf_term.methods._methods.rankingdata import RankingData


class MethodLayerRankingNoCache(BaseMethodLayerRankingCache):
    def __init__(self, cache_dir: str) -> None:
        pass

    def load(
        self,
        pdf_paths: List[str],
        config: MethodLayerConfig,
    ) -> Union[MethodTermRanking, None]:
        pass

    def store(
        self,
        pdf_paths: List[str],
        term_ranking: MethodTermRanking,
        config: MethodLayerConfig,
    ) -> None:
        pass

    def remove(self, pdf_paths: List[str], config: MethodLayerConfig) -> None:
        pass


class MethodLayerDataNoCache(BaseMethodLayerDataCache[RankingData]):
    def __init__(self, cache_dir: str) -> None:
        pass

    def load(
        self,
        pdf_paths: List[str],
        config: MethodLayerConfig,
        from_dict: Callable[[Dict[str, Any]], RankingData],
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
