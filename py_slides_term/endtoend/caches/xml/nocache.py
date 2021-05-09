from typing import Union

from .base import BaseXMLLayerCache
from ...configs import XMLLayerConfig
from py_slides_term.pdftoxml import PDFnXMLElement


class XMLLayerNoCache(BaseXMLLayerCache):
    # public
    def __init__(self, cache_dirlike: str):
        pass

    def load(
        self, pdf_path: str, config: XMLLayerConfig
    ) -> Union[PDFnXMLElement, None]:
        pass

    def store(self, pdfnxml: PDFnXMLElement, config: XMLLayerConfig) -> None:
        pass

    def remove(self, pdf_path: str, config: XMLLayerConfig) -> None:
        pass
