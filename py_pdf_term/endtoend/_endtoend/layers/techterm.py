from typing import List, Optional

from py_pdf_term.techterms import PDFTechnicalTermList, TechnicalTermExtractor

from ..configs import TechnicalTermLayerConfig
from ..data import DomainPDFList
from .candidate import CandidateLayer
from .method import MethodLayer
from .styling import StylingLayer


class TechnicalTermLayer:
    def __init__(
        self,
        candidate_layer: CandidateLayer,
        method_layer: MethodLayer,
        styling_layer: StylingLayer,
        config: Optional[TechnicalTermLayerConfig] = None,
    ) -> None:
        if config is None:
            config = TechnicalTermLayerConfig()

        self._techterm = TechnicalTermExtractor(
            max_num_terms=config.max_num_terms,
            acceptance_rate=config.acceptance_rate,
        )
        self._config = config

        self._candidate_layer = candidate_layer
        self._method_layer = method_layer
        self._styling_layer = styling_layer

    def create_pdf_techterms(
        self,
        domain: str,
        pdf_path: str,
        single_domain_pdfs: Optional[DomainPDFList] = None,
        multi_domain_pdfs: Optional[List[DomainPDFList]] = None,
    ) -> PDFTechnicalTermList:
        pdf_candidates = self._candidate_layer.create_pdf_candidates(pdf_path)
        term_ranking = self._method_layer.create_term_ranking(
            domain, single_domain_pdfs, multi_domain_pdfs
        )
        pdf_styling_scores = self._styling_layer.create_pdf_styling_scores(pdf_path)
        techterms = self._techterm.extract_from_pdf(
            pdf_candidates, term_ranking, pdf_styling_scores
        )

        return techterms
