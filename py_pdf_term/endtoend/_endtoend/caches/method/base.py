from abc import ABCMeta, abstractmethod
from typing import Any, Callable

from py_pdf_term.methods import MethodTermRanking
from py_pdf_term.methods._methods.rankingdata import BaseRankingData

from ...configs import BaseMethodLayerConfig


class BaseMethodLayerRankingCache(metaclass=ABCMeta):
    """Base class for method layer ranking caches. A method layer ranking cache is
    expected to store and load term rankings per a domain of PDF files.

    Args
    ----
        cache_dir:
            Directory path to store cache files.
    """

    def __init__(self, cache_dir: str) -> None:
        pass

    @abstractmethod
    def load(
        self,
        pdf_paths: list[str],
        config: BaseMethodLayerConfig,
    ) -> MethodTermRanking | None:
        """Load term rankings from a cache file.

        Args
        ----
            pdf_paths:
                Paths to PDF files in a domain to load term rankings. The order of
                the paths is important. The order should be the same as that when the
                store method is called.
            config:
                Configuration for the method layer. The configuration is used to
                determine the cache file path.

        Returns
        -------
            MethodTermRanking | None:
                Loaded term rankings. If there is no cache file, this method returns
                None.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.load()")

    @abstractmethod
    def store(
        self,
        pdf_paths: list[str],
        term_ranking: MethodTermRanking,
        config: BaseMethodLayerConfig,
    ) -> None:
        """Store term rankings to a cache file.

        Args
        ----
            pdf_paths:
                Paths to PDF files in a domain to store term rankings. The order of
                the paths is important. The order should be the same as that when the
                load method to be called.
            term_ranking:
                Term rankings to store.
            config:
                Configuration for the method layer. The configuration is used to
                determine the cache file path.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.store()")

    @abstractmethod
    def remove(self, pdf_paths: list[str], config: BaseMethodLayerConfig) -> None:
        """Remove cache file.

        Args
        ----
            pdf_paths:
                Paths to PDF files in a domain to remove cache files. The order of
                the paths is important. The order should be the same as that when the
                store method called.
            config:
                Configuration for the method layer. The configuration is used to
                determine the cache file path.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.remove()")


class BaseMethodLayerDataCache[RankingData: BaseRankingData](metaclass=ABCMeta):
    """Base class for method layer data caches. A method layer data cache is expected
    to store and load metadata to generate term rankings per a domain of PDF files.

    Args
    ----
        cache_dir:
            Directory path to store cache files.
    """

    def __init__(self, cache_dir: str) -> None:
        pass

    @abstractmethod
    def load(
        self,
        pdf_paths: list[str],
        config: BaseMethodLayerConfig,
        from_dict: Callable[[dict[str, Any]], RankingData],
    ) -> RankingData | None:
        """Load metadata to generate term rankings from a cache file.

        Args
        ----
            pdf_paths:
                Paths to PDF files in a domain to load metadata. The order of the
                paths is important. The order should be the same as that when the store
                method is called.
            config:
                Configuration for the method layer. The configuration is used to
                determine the cache file path.
            from_dict:
                Function to convert a dictionary to a RankingData object.

        Returns
        -------
            RankingData | None:
                Loaded metadata to generate term rankings. If there is no cache
                file, this method returns None. The returned metadata is converted to
                a RankingData object by the from_dict function.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.load()")

    @abstractmethod
    def store(
        self,
        pdf_paths: list[str],
        ranking_data: RankingData,
        config: BaseMethodLayerConfig,
    ) -> None:
        """Store metadata to generate term rankings to a cache file.

        Args
        ----
            pdf_paths:
                Paths to PDF files in a domain to store metadata. The order of the
                paths is important. The order should be the same as that when the load
                method to be called.
            ranking_data:
                Metadata to generate term rankings to store.
            config:
                Configuration for the method layer. The configuration is used to
                determine the cache file path.
        """
        raise NotImplementedError(f"{self.__class__.__name__}.store()")

    @abstractmethod
    def remove(self, pdf_paths: list[str], config: BaseMethodLayerConfig) -> None:
        """Remove cache file.

        Args
        ----
            pdf_paths:
                Paths to PDF files in a domain to remove cache files. The order of
                the paths is important. The order should be the same as that when the
                store method called.
            config:
                Configuration for the method layer. The configuration is used to
                determine the cache file path.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.remove()")
