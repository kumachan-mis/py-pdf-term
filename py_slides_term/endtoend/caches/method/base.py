from abc import ABCMeta, abstractmethod
from typing import List, Dict, Any, Union, Callable, Generic

from ...configs import MethodLayerConfig
from py_slides_term.methods import DomainTermRanking
from py_slides_term.methods.rankingdata import RankingData


class BaseMethodLayerRankingCache(metaclass=ABCMeta):
    # public
    def __init__(self, cache_dir: str):
        pass

    @abstractmethod
    def load(
        self,
        pdf_paths: List[str],
        config: MethodLayerConfig,
    ) -> Union[DomainTermRanking, None]:
        raise NotImplementedError(f"{self.__class__.__name__}.load()")

    @abstractmethod
    def store(
        self,
        pdf_paths: List[str],
        term_ranking: DomainTermRanking,
        config: MethodLayerConfig,
    ) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.store()")

    @abstractmethod
    def remove(self, pdf_paths: List[str], config: MethodLayerConfig) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.remove()")


class BaseMethodLayerDataCache(Generic[RankingData], metaclass=ABCMeta):
    # public
    def __init__(self, cache_dir: str):
        pass

    @abstractmethod
    def load(
        self,
        pdf_paths: List[str],
        config: MethodLayerConfig,
        from_json: Callable[[Dict[str, Any]], RankingData],
    ) -> Union[RankingData, None]:
        raise NotImplementedError(f"{self.__class__.__name__}.load()")

    @abstractmethod
    def store(
        self,
        pdf_paths: List[str],
        ranking_data: RankingData,
        config: MethodLayerConfig,
    ) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.store()")

    @abstractmethod
    def remove(self, pdf_paths: List[str], config: MethodLayerConfig) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.remove()")