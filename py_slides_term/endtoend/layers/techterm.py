from typing import List, Optional

from ..configs import TechnicalTermLayerConfig
from ..data import DomainPDFList
from .candidate import CandidateLayer
from .method import MethodLayer
from py_slides_term.techterms import TechnicalTermExtractor, PDFTechnicalTermList


class TechnicalTermLayer:
    # public
    def __init__(
        self,
        candidate_layer: CandidateLayer,
        method_layer: MethodLayer,
        config: Optional[TechnicalTermLayerConfig] = None,
    ):
        if config is None:
            config = TechnicalTermLayerConfig()

        self._techterm = TechnicalTermExtractor(
            max_num_pageterms=config.max_num_pageterms,
            acceptance_rate=config.acceptance_rate,
        )
        self._config = config

        self._candidate_layer = candidate_layer
        self._method_layer = method_layer

    def create_pdf_techterms(
        self,
        domain: str,
        pdf_path: str,
        single_domain_pdfs: Optional[DomainPDFList] = None,
        multi_domain_pdfs: Optional[List[DomainPDFList]] = None,
    ) -> PDFTechnicalTermList:
        pdf_candidate = self._candidate_layer.create_pdf_candidates(pdf_path)
        term_ranking = self._method_layer.create_term_ranking(
            domain, single_domain_pdfs, multi_domain_pdfs
        )
        techterms = self._techterm.extract_from_pdf(pdf_candidate, term_ranking)

        if self._config.remove_lower_layer_cache:
            if single_domain_pdfs is not None:
                domain_pdfs = single_domain_pdfs
                self._method_layer.remove_cache(domain_pdfs.pdf_paths)
            if multi_domain_pdfs is not None:
                domain_pdfs = next(
                    filter(lambda item: item.domain == domain, multi_domain_pdfs)
                )
                self._method_layer.remove_cache(domain_pdfs.pdf_paths)

        return techterms
