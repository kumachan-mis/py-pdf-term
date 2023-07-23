from abc import ABCMeta

from py_pdf_term.techterms import PDFTechnicalTermList, TechnicalTermExtractor

from ..configs import TechnicalTermLayerConfig
from ..data import DomainPDFList
from .candidate import CandidateLayer
from .method import MultiDomainMethodLayer, SingleDomainMethodLayer
from .styling import StylingLayer


class BaseTechnicalTermLayer(metaclass=ABCMeta):
    """Base class for technical term layers to extract technical terms from candidate
    terms using candidate layer and styling layer.

    Args
    ----
        candidate_layer:
            Layer to extract candidate terms.
        styling_layer:
            Layer to calculate styling scores.
        config:
            Configuration for this layer. If None, the default configuration is used.
    """

    def __init__(
        self,
        candidate_layer: CandidateLayer,
        styling_layer: StylingLayer,
        config: TechnicalTermLayerConfig | None = None,
    ) -> None:
        if config is None:
            config = TechnicalTermLayerConfig()

        self._techterm = TechnicalTermExtractor(
            max_num_terms=config.max_num_terms,
            acceptance_rate=config.acceptance_rate,
        )
        self._config = config

        self._candidate_layer = candidate_layer
        self._styling_layer = styling_layer


class SingleDomainTechnicalTermLayer(BaseTechnicalTermLayer):
    """Technical term layer to extract technical terms from candidate terms using
    candidate layer, single domain method layer and styling layer.

    Args
    ----
        candidate_layer:
            Layer to extract candidate terms.
        method_layer:
            Layer to calculate term ranking which does not require cross-domain
            information.
        styling_layer:
            Layer to calculate styling scores.
        config:
            Configuration for this layer. If None, the default configuration is used.
    """

    def __init__(
        self,
        candidate_layer: CandidateLayer,
        method_layer: SingleDomainMethodLayer,
        styling_layer: StylingLayer,
        config: TechnicalTermLayerConfig | None = None,
    ) -> None:
        super().__init__(candidate_layer, styling_layer, config)

        self._method_layer = method_layer

    def create_pdf_techterms(
        self, pdf_path: str, domain_pdfs: DomainPDFList
    ) -> PDFTechnicalTermList:
        """Extract technical terms from a PDF file in a domain.

        Args
        ----
            pdf_path:
                PDF path to extract technical terms.
            domain_pdfs:
                List of PDF paths in a domain. This is used to calculate term ranking.
                This must contain the PDF path to extract technical terms.

        Returns
        -------
            PDFTechnicalTermList:
                List of technical terms extracted from the PDF file.
        """

        pdf_candidates = self._candidate_layer.create_pdf_candidates(pdf_path)
        term_ranking = self._method_layer.create_term_ranking(domain_pdfs)
        pdf_styling_scores = self._styling_layer.create_pdf_styling_scores(pdf_path)
        techterms = self._techterm.extract_from_pdf(
            pdf_candidates, term_ranking, pdf_styling_scores
        )

        return techterms


class MultiDomainTechnicalTermLayer(BaseTechnicalTermLayer):
    """Technical term layer to extract technical terms from candidate terms using
    candidate layer, multi domain method layer and styling layer.

    Args
    ----
        candidate_layer:
            Layer to extract candidate terms.
        method_layer:
            Layer to calculate term ranking which requires cross-domain information.
        styling_layer:
            Layer to calculate styling scores.
        config:
            Configuration for this layer. If None, the default configuration is used.
    """

    def __init__(
        self,
        candidate_layer: CandidateLayer,
        method_layer: MultiDomainMethodLayer,
        styling_layer: StylingLayer,
        config: TechnicalTermLayerConfig | None = None,
    ) -> None:
        super().__init__(candidate_layer, styling_layer, config)

        self._method_layer = method_layer

    def create_pdf_techterms(
        self, domain: str, pdf_path: str, multi_domain_pdfs: list[DomainPDFList]
    ) -> PDFTechnicalTermList:
        """Extract technical terms from a PDF file in a domain.

        Args
        ----
            domain:
                Domain to extract technical terms.
            pdf_path:
                PDF path to extract technical terms. This PDF file is in the domain.
            multi_domain_pdfs:
                List of PDF paths in each domain. The PDF file in the domain must be
                included in this list.

        Returns
        -------
            PDFTechnicalTermList:
                List of technical terms extracted from the PDF file.
        """

        pdf_candidates = self._candidate_layer.create_pdf_candidates(pdf_path)
        term_ranking = self._method_layer.create_term_ranking(domain, multi_domain_pdfs)
        pdf_styling_scores = self._styling_layer.create_pdf_styling_scores(pdf_path)
        techterms = self._techterm.extract_from_pdf(
            pdf_candidates, term_ranking, pdf_styling_scores
        )

        return techterms
