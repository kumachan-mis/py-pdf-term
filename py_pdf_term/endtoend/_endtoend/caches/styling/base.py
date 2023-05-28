from abc import ABCMeta, abstractmethod

from py_pdf_term.stylings import PDFStylingScoreList

from ...configs import StylingLayerConfig


class BaseStylingLayerCache(metaclass=ABCMeta):
    """Base class for styling layer caches. A styling layer cache is expected to store
    and load styling scores per a PDF file.

    Args
    ----
        cache_dir:
            Directory path to store cache files.

    """

    def __init__(self, cache_dir: str) -> None:
        pass

    @abstractmethod
    def load(
        self, pdf_path: str, config: StylingLayerConfig
    ) -> PDFStylingScoreList | None:
        """Load styling scores from a cache file.

        Args
        ----
            pdf_path:
                Path to a PDF file to load styling scores.
            config:
                Configuration for the styling layer. The configuration is used to
                determine the cache file path.

        Returns
        -------
            PDFStylingScoreList | None:
                Loaded styling scores. If there is no cache file, this method
                returns None.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.load()")

    @abstractmethod
    def store(
        self, styling_scores: PDFStylingScoreList, config: StylingLayerConfig
    ) -> None:
        """Store styling scores to a cache file.

        Args
        ----
            styling_scores:
                Styling scores to store.
            config:
                Configuration for the styling layer. The configuration is used to
                determine the cache file path.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.store()")

    @abstractmethod
    def remove(self, pdf_path: str, config: StylingLayerConfig) -> None:
        """Remove a cache file.

        Args
        ----
            pdf_path:
                Path to a PDF file to remove a cache file.
            config:
                Configuration for the styling layer. The configuration is used to
                determine the cache file path.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.remove()")
