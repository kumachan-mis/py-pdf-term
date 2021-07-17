from typing import Union

from .base import BaseCandidateLayerCache
from ...configs import CandidateLayerConfig
from py_pdf_term.candidates import PDFCandidateTermList


class CandidateLayerNoCache(BaseCandidateLayerCache):
    def __init__(self, cache_dir: str) -> None:
        pass

    def load(
        self, pdf_path: str, config: CandidateLayerConfig
    ) -> Union[PDFCandidateTermList, None]:
        pass

    def store(
        self, candidates: PDFCandidateTermList, config: CandidateLayerConfig
    ) -> None:
        pass

    def remove(self, pdf_path: str, config: CandidateLayerConfig) -> None:
        pass
