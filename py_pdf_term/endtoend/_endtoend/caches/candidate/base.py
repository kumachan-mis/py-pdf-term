from abc import ABCMeta, abstractmethod
from typing import Union

from py_pdf_term.candidates import PDFCandidateTermList

from ...configs import CandidateLayerConfig


class BaseCandidateLayerCache(metaclass=ABCMeta):
    """Base class for candidate layer caches. A candidate layer cache is expected to
    store and load candidate terms per a PDF file.

    Args
    ----
        cache_dir:
            The directory path to store cache files.
    """

    def __init__(self, cache_dir: str) -> None:
        pass

    @abstractmethod
    def load(
        self, pdf_path: str, config: CandidateLayerConfig
    ) -> Union[PDFCandidateTermList, None]:
        """Load candidate terms from a cache file.

        Args
        ----
            pdf_path:
                The path to a PDF file to load candidate terms.
            config:
                The configuration for the candidate layer. The configuration is used to
                determine the cache file path.

        Returns
        -------
            Union[PDFCandidateTermList, None]:
                The loaded candidate terms. If there is no cache file, this method
                returns None.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.load()")

    @abstractmethod
    def store(
        self, candidates: PDFCandidateTermList, config: CandidateLayerConfig
    ) -> None:
        """Store candidate terms to a cache file.

        Args
        ----
            candidates:
                The candidate terms to store.
            config:
                The configuration for the candidate layer. The configuration is used to
                determine the cache file path.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.store()")

    @abstractmethod
    def remove(self, pdf_path: str, config: CandidateLayerConfig) -> None:
        """Remove a cache file.

        Args
        ----
            pdf_path:
                The path to a PDF file to remove a cache file.
            config:
                The configuration for the candidate layer. The configuration is used to
                determine the cache file path.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.remove()")
