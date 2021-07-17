from typing import Union

from .base import BaseXMLLayerCache
from ...configs import XMLLayerConfig
from py_pdf_term.pdftoxml import PDFnXMLElement


class XMLLayerNoCache(BaseXMLLayerCache):
    def __init__(self, cache_dir: str) -> None:
        pass

    def load(
        self, pdf_path: str, config: XMLLayerConfig
    ) -> Union[PDFnXMLElement, None]:
        pass

    def store(self, pdfnxml: PDFnXMLElement, config: XMLLayerConfig) -> None:
        pass

    def remove(self, pdf_path: str, config: XMLLayerConfig) -> None:
        pass
