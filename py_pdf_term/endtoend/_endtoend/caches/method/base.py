from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Dict, Generic, List, Union

from py_pdf_term.methods import MethodTermRanking
from py_pdf_term.methods._methods.rankingdata import RankingData

from ...configs import BaseMethodLayerConfig


class BaseMethodLayerRankingCache(metaclass=ABCMeta):
    def __init__(self, cache_dir: str) -> None:
        pass

    @abstractmethod
    def load(
        self,
        pdf_paths: List[str],
        config: BaseMethodLayerConfig,
    ) -> Union[MethodTermRanking, None]:
        raise NotImplementedError(f"{self.__class__.__name__}.load()")

    @abstractmethod
    def store(
        self,
        pdf_paths: List[str],
        term_ranking: MethodTermRanking,
        config: BaseMethodLayerConfig,
    ) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.store()")

    @abstractmethod
    def remove(self, pdf_paths: List[str], config: BaseMethodLayerConfig) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.remove()")


class BaseMethodLayerDataCache(Generic[RankingData], metaclass=ABCMeta):
    def __init__(self, cache_dir: str) -> None:
        pass

    @abstractmethod
    def load(
        self,
        pdf_paths: List[str],
        config: BaseMethodLayerConfig,
        from_dict: Callable[[Dict[str, Any]], RankingData],
    ) -> Union[RankingData, None]:
        raise NotImplementedError(f"{self.__class__.__name__}.load()")

    @abstractmethod
    def store(
        self,
        pdf_paths: List[str],
        ranking_data: RankingData,
        config: BaseMethodLayerConfig,
    ) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.store()")

    @abstractmethod
    def remove(self, pdf_paths: List[str], config: BaseMethodLayerConfig) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.remove()")
