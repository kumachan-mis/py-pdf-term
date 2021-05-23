from typing import Union

from .base import BaseCandidateLayerCache
from ...configs import CandidateLayerConfig
from py_slides_term.candidates import PDFCandidateTermList


class CandidateLayerNoCache(BaseCandidateLayerCache):
    def __init__(self, cache_dir: str):
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
