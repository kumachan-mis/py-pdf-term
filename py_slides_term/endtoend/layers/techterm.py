from typing import Optional

from ..configs import TechnicalTermLayerConfig
from py_slides_term.candidates import PDFCandidateTermList
from py_slides_term.methods import DomainTermRanking
from py_slides_term.techterms import TechnicalTermExtractor, PDFTechnicalTermList


class TechnicalTermLayer:
    def __init__(self, config: Optional[TechnicalTermLayerConfig] = None):
        if config is None:
            config = TechnicalTermLayerConfig()

        self._techterm = TechnicalTermExtractor(
            max_num_pageterms=config.max_num_pageterms,
            acceptance_rate=config.acceptance_rate,
        )
        self._config = config

    def process(
        self, pdf_candidate: PDFCandidateTermList, term_ranking: DomainTermRanking
    ) -> PDFTechnicalTermList:
        techterms = self._techterm.extract_from_pdf(pdf_candidate, term_ranking)
        return techterms
