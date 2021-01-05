from typing import List, Optional

from .configs import (
    XMLLayerConfig,
    CandidateLayerConfig,
    RankingMethodLayerConfig,
    TechnicalTermLayerConfig,
)
from .mappers import (
    CandidateMorphemeFilterMapper,
    CandidateTermFilterMapper,
    SingleDomainRankingMethodMapper,
    MultiDomainRankingMethodMapper,
)
from .layers import XMLLayer, CandidateLayer, RankingMethodLayer, TechnicalTermLayer
from .caches import DEFAULT_CACHE_DIR
from .data import DomainPDFList
from py_slides_term.candidates import DomainCandidateTermList, PDFCandidateTermList
from py_slides_term.techterms import PDFTechnicalTermList


class PySlidesTermExtractor:
    def __init__(
        self,
        xml_config: Optional[XMLLayerConfig] = None,
        candidate_config: Optional[CandidateLayerConfig] = None,
        method_config: Optional[RankingMethodLayerConfig] = None,
        techterm_config: Optional[TechnicalTermLayerConfig] = None,
        morpheme_filter_mapper: Optional[CandidateMorphemeFilterMapper] = None,
        term_filter_mapper: Optional[CandidateTermFilterMapper] = None,
        single_method_mapper: Optional[SingleDomainRankingMethodMapper] = None,
        multi_method_mapper: Optional[MultiDomainRankingMethodMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ):
        self._xml_layer = XMLLayer(xml_config, cache_dir)
        self._candidate_layer = CandidateLayer(
            candidate_config, morpheme_filter_mapper, term_filter_mapper, cache_dir
        )
        self._method_layer = RankingMethodLayer(
            method_config, single_method_mapper, multi_method_mapper, cache_dir
        )
        self._techterm_layer = TechnicalTermLayer(techterm_config)

        self._method_type = self._method_layer.method_type

    def extract(
        self,
        domain: str,
        pdf_path: str,
        single_domain_pdfs: Optional[DomainPDFList] = None,
        multi_domain_pdfs: Optional[List[DomainPDFList]] = None,
    ) -> PDFTechnicalTermList:
        if self._method_type == "single":
            if single_domain_pdfs is None:
                raise ValueError(
                    "'single_domain_pdfs' is required"
                    "when using single-domain ranking method"
                )

            return self._run_single_domain_method(domain, pdf_path, single_domain_pdfs)
        elif self._method_type == "multi":
            if multi_domain_pdfs is None:
                raise ValueError(
                    "'multi_domain_pdfs' is required"
                    " when using  multi-domain ranking method"
                )

            return self._run_multi_domain_method(domain, pdf_path, multi_domain_pdfs)
        else:
            raise RuntimeError("unreachable statement")

    # private
    def _run_single_domain_method(
        self,
        domain: str,
        pdf_path: str,
        single_domain_pdfs: DomainPDFList,
    ) -> PDFTechnicalTermList:
        if domain != single_domain_pdfs.domain:
            raise ValueError(
                f"domain of 'single_domain_pdfs is expected to be '{domain}'"
                f" but got '{single_domain_pdfs.domain}'"
            )

        if pdf_path not in single_domain_pdfs.pdf_paths:
            raise ValueError(f"single_domain_pdfs does not contain '{pdf_path}'")

        pdf_candidates_list: List[PDFCandidateTermList] = []
        for _pdf_path in single_domain_pdfs.pdf_paths:
            pdfnxml = self._xml_layer.process(_pdf_path)
            pdf_candidates = self._candidate_layer.process(pdfnxml)
            pdf_candidates_list.append(pdf_candidates)

        domain_candidates = DomainCandidateTermList(domain, pdf_candidates_list)
        pdf_candidates = next(
            filter(lambda item: item.pdf_path == pdf_path, domain_candidates.pdfs)
        )
        term_ranking = self._method_layer.process(
            domain, single_domain_candidates=domain_candidates
        )
        techterms = self._techterm_layer.process(pdf_candidates, term_ranking)
        return techterms

    def _run_multi_domain_method(
        self,
        domain: str,
        pdf_path: str,
        multi_domain_pdfs: List[DomainPDFList],
    ) -> PDFTechnicalTermList:
        domain_pdfs = next(
            filter(lambda pdfs: pdfs.domain == domain, multi_domain_pdfs),
            None,
        )
        if domain_pdfs is None:
            raise ValueError(f"'multi_domain_pdfs' does not contain domain '{domain}'")

        if pdf_path not in domain_pdfs.pdf_paths:
            raise ValueError(f"domain_pdfs in '{domain}' does not contain '{pdf_path}'")

        domain_candidates_list: List[DomainCandidateTermList] = []
        for domain_pdfs in multi_domain_pdfs:
            pdf_candidates_list: List[PDFCandidateTermList] = []
            for _pdf_path in domain_pdfs.pdf_paths:
                pdfnxml = self._xml_layer.process(_pdf_path)
                pdf_candidates = self._candidate_layer.process(pdfnxml)
                pdf_candidates_list.append(pdf_candidates)

            domain_candidates = DomainCandidateTermList(domain, pdf_candidates_list)
            domain_candidates_list.append(domain_candidates)

        domain_candidates = next(
            filter(lambda item: item.domain == domain, domain_candidates_list)
        )
        pdf_candidates = next(
            filter(lambda pdf: pdf.pdf_path == pdf_path, domain_candidates.pdfs)
        )
        term_ranking = self._method_layer.process(
            domain, multi_domain_candidates=domain_candidates_list
        )
        techterms = self._techterm_layer.process(pdf_candidates, term_ranking)
        return techterms
