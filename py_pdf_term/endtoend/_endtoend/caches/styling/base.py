from abc import ABCMeta, abstractmethod
from typing import Union

from py_pdf_term.stylings import PDFStylingScoreList

from ...configs import StylingLayerConfig


class BaseStylingLayerCache(metaclass=ABCMeta):
    def __init__(self, cache_dir: str) -> None:
        pass

    @abstractmethod
    def load(
        self, pdf_path: str, config: StylingLayerConfig
    ) -> Union[PDFStylingScoreList, None]:
        raise NotImplementedError(f"{self.__class__.__name__}.load()")

    @abstractmethod
    def store(
        self, styling_scores: PDFStylingScoreList, config: StylingLayerConfig
    ) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.store()")

    @abstractmethod
    def remove(self, pdf_path: str, config: StylingLayerConfig) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.remove()")
