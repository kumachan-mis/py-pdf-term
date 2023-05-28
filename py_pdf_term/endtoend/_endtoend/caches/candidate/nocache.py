from py_pdf_term.candidates import PDFCandidateTermList

from ...configs import CandidateLayerConfig
from .base import BaseCandidateLayerCache


class CandidateLayerNoCache(BaseCandidateLayerCache):
    """Candidate layer cache that does not store and load candidate terms.

    Args
    ----
        cache_dir:
            This argument is ignored.
    """

    def __init__(self, cache_dir: str) -> None:
        pass

    def load(
        self, pdf_path: str, config: CandidateLayerConfig
    ) -> PDFCandidateTermList | None:
        pass

    def store(
        self, candidates: PDFCandidateTermList, config: CandidateLayerConfig
    ) -> None:
        pass

    def remove(self, pdf_path: str, config: CandidateLayerConfig) -> None:
        pass
