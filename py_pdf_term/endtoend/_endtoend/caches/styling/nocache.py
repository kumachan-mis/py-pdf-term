from py_pdf_term.stylings import PDFStylingScoreList

from ...configs import StylingLayerConfig
from .base import BaseStylingLayerCache


class StylingLayerNoCache(BaseStylingLayerCache):
    """Styling layer cache that does not store and load styling scores.

    Args
    ----
        cache_dir:
            This argument is ignored.
    """

    def __init__(self, cache_dir: str) -> None:
        pass

    def load(
        self, pdf_path: str, config: StylingLayerConfig
    ) -> PDFStylingScoreList | None:
        pass

    def store(
        self, styling_scores: PDFStylingScoreList, config: StylingLayerConfig
    ) -> None:
        pass

    def remove(self, pdf_path: str, config: StylingLayerConfig) -> None:
        pass
