from py_pdf_term.pdftoxml import PDFnXMLElement

from ...configs import XMLLayerConfig
from .base import BaseXMLLayerCache


class XMLLayerNoCache(BaseXMLLayerCache):
    """An XML layer cache that does not store and load XML elements.

    Args
    ----
        cache_dir:
            This argument is ignored.
    """

    def __init__(self, cache_dir: str) -> None:
        pass

    def load(self, pdf_path: str, config: XMLLayerConfig) -> PDFnXMLElement | None:
        pass

    def store(self, pdfnxml: PDFnXMLElement, config: XMLLayerConfig) -> None:
        pass

    def remove(self, pdf_path: str, config: XMLLayerConfig) -> None:
        pass
