from abc import ABCMeta, abstractmethod
from typing import Union

from ...configs import CandidateLayerConfig
from py_pdf_term.candidates import PDFCandidateTermList


class BaseCandidateLayerCache(metaclass=ABCMeta):
    def __init__(self, cache_dir: str) -> None:
        pass

    @abstractmethod
    def load(
        self, pdf_path: str, config: CandidateLayerConfig
    ) -> Union[PDFCandidateTermList, None]:
        raise NotImplementedError(f"{self.__class__.__name__}.load()")

    @abstractmethod
    def store(
        self, candidates: PDFCandidateTermList, config: CandidateLayerConfig
    ) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.store()")

    @abstractmethod
    def remove(self, pdf_path: str, config: CandidateLayerConfig) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.remove()")
