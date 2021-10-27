from abc import ABCMeta, abstractmethod
from typing import Union

from py_pdf_term.pdftoxml import PDFnXMLElement

from ...configs import XMLLayerConfig


class BaseXMLLayerCache(metaclass=ABCMeta):
    def __init__(self, cache_dir: str) -> None:
        pass

    @abstractmethod
    def load(
        self, pdf_path: str, config: XMLLayerConfig
    ) -> Union[PDFnXMLElement, None]:
        raise NotImplementedError(f"{self.__class__.__name__}.load()")

    @abstractmethod
    def store(self, pdfnxml: PDFnXMLElement, config: XMLLayerConfig) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.store()")

    @abstractmethod
    def remove(self, pdf_path: str, config: XMLLayerConfig) -> None:
        raise NotImplementedError(f"{self.__class__.__name__}.remove()")
