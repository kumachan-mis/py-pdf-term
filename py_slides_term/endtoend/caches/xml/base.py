from abc import ABCMeta, abstractmethod
from typing import Union

from ...configs import XMLLayerConfig
from py_slides_term.pdftoxml import PDFnXMLElement


class BaseXMLLayerCache(metaclass=ABCMeta):
    # public
    def __init__(self, cache_dir: str):
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
