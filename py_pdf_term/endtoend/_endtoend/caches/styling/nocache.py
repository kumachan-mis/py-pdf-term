from typing import Union

from .base import BaseStylingLayerCache
from ...configs import StylingLayerConfig
from py_pdf_term.stylings import PDFStylingScoreList


class StylingLayerNoCache(BaseStylingLayerCache):
    def __init__(self, cache_dir: str) -> None:
        pass

    def load(
        self, pdf_path: str, config: StylingLayerConfig
    ) -> Union[PDFStylingScoreList, None]:
        pass

    def store(
        self, styling_scores: PDFStylingScoreList, config: StylingLayerConfig
    ) -> None:
        pass

    def remove(self, pdf_path: str, config: StylingLayerConfig) -> None:
        pass
