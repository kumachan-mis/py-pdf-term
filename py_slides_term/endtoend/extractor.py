from typing import List, Any, Optional, Union

from .configs import (
    XMLConfig,
    CandidateConfig,
    RankingMethodConfig,
    TechnicalTermConfig,
)
from .mappers import CandidateFilterMapper, RankingMethodMapper
from .cache import PySlidesTermCache, DEFAULT_CACHE_DIR
from .data import DomainPDFList
from py_slides_term.pdftoxml import PDFtoXMLConverter
from py_slides_term.candidates import (
    CandidateTermExtractor,
    BaseCandidateMorphemeFilter,
    BaseCandidateTermFilter,
    DomainCandidateTermList,
    PDFCandidateTermList,
)
from py_slides_term.methods import (
    BaseSingleDomainRankingMethod,
    BaseMultiDomainRankingMethod,
)
from py_slides_term.techterms import TechnicalTermExtractor, PDFTechnicalTermList


class PySlidesTermExtractor:
    # public
    def __init__(
        self,
        xml_config: Optional[XMLConfig] = None,
        candidates_config: Optional[CandidateConfig] = None,
        method_config: Optional[RankingMethodConfig] = None,
        techterm_config: Optional[TechnicalTermConfig] = None,
        filter_mapper: Optional[CandidateFilterMapper] = None,
        method_mapper: Optional[RankingMethodMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ):
        if xml_config is None:
            xml_config = XMLConfig()
        if candidates_config is None:
            candidates_config = CandidateConfig()
        if method_config is None:
            method_config = RankingMethodConfig()
        if techterm_config is None:
            techterm_config = TechnicalTermConfig()

        self._xml_config = xml_config
        self._candidates_config = candidates_config
        self._method_config = method_config
        self._techterm_config = techterm_config

        self._xml = self.create_xml(xml_config)
        self._candidates = self.create_candidates(candidates_config, filter_mapper)
        self._method = self.create_method(method_config, method_mapper)
        self._techterm = self.create_techterm(techterm_config)

        self._cache = PySlidesTermCache(cache_dir)

    @classmethod
    def create_xml(
        cls,
        config: Optional[XMLConfig] = None,
    ) -> PDFtoXMLConverter:
        if config is None:
            config = XMLConfig()

        return PDFtoXMLConverter()

    @classmethod
    def create_candidates(
        cls,
        config: Optional[CandidateConfig] = None,
        filter_mapper: Optional[CandidateFilterMapper] = None,
    ) -> CandidateTermExtractor:
        if config is None:
            config = CandidateConfig()
        if filter_mapper is None:
            filter_mapper = CandidateFilterMapper.default_mapper()

        morpheme_filters: List[BaseCandidateMorphemeFilter] = []
        for cls_name in config.morpheme_filters:
            morpheme_filter_cls = filter_mapper.find_morpheme_filter_cls(cls_name)
            if morpheme_filter_cls is None:
                raise ValueError(f"morpheme filter named '{cls_name}' not found")

            morpheme_filters.append(morpheme_filter_cls())

        term_filters: List[BaseCandidateTermFilter] = []
        for cls_name in config.term_filters:
            term_filter_cls = filter_mapper.find_term_filter_cls(cls_name)
            if term_filter_cls is None:
                raise ValueError(f"term filter named '{cls_name}' not found")

            term_filters.append(term_filter_cls())

        return CandidateTermExtractor(
            morpheme_filters=morpheme_filters,
            term_filters=term_filters,
            modifying_particle_augmentation=config.modifying_particle_augmentation,
        )

    @classmethod
    def create_method(
        cls,
        config: Optional[RankingMethodConfig] = None,
        method_mapper: Optional[RankingMethodMapper] = None,
    ) -> Union[BaseSingleDomainRankingMethod[Any], BaseMultiDomainRankingMethod[Any]]:
        if config is None:
            config = RankingMethodConfig()
        if method_mapper is None:
            method_mapper = RankingMethodMapper.default_mapper()

        if config.type == "single":
            method_cls = method_mapper.find_single_domain_method_cls(config.method)
        elif config.type == "multi":
            method_cls = method_mapper.find_multi_domain_method_cls(config.method)
        else:
            raise ValueError(f"method type '{config.type}' is unknown")

        if method_cls is None:
            raise ValueError(f"method named '{config.method}' not found")

        return method_cls(**config.hyper_params)

    @classmethod
    def create_techterm(
        cls,
        config: Optional[TechnicalTermConfig] = None,
    ) -> TechnicalTermExtractor:
        if config is None:
            config = TechnicalTermConfig()

        return TechnicalTermExtractor(
            max_num_pageterms=config.max_num_pageterms,
            acceptance_rate=config.acceptance_rate,
        )

    def extract(
        self,
        domain: str,
        pdf_path: str,
        single_domain_pdfs: Optional[DomainPDFList] = None,
        multi_domain_pdfs: Optional[List[DomainPDFList]] = None,
    ) -> PDFTechnicalTermList:
        # pyright:reportUnnecessaryIsInstance=false
        if isinstance(self._method, BaseSingleDomainRankingMethod):
            if single_domain_pdfs is None:
                raise ValueError(
                    "'single_domain_pdfs' is required"
                    "when using single-domain ranking method"
                )
            return self._run_single_domain_method(domain, pdf_path, single_domain_pdfs)
        elif isinstance(self._method, BaseMultiDomainRankingMethod):
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
        if not isinstance(self._method, BaseSingleDomainRankingMethod):
            raise RuntimeError("unreachable statement")

        if domain != single_domain_pdfs.domain:
            raise ValueError(
                f"domain of 'single_domain_pdfs is expected to be '{domain}'"
                f" but got '{single_domain_pdfs.domain}'"
            )

        if pdf_path not in single_domain_pdfs.pdf_paths:
            raise ValueError(f"single_domain_pdfs does not contain '{pdf_path}'")

        domain_candidates = self._create_domain_candidates(single_domain_pdfs)
        pdf_candidates = next(
            filter(lambda pdf: pdf.pdf_path == pdf_path, domain_candidates.pdfs)
        )
        ranking = self._method.rank_terms(domain_candidates)
        techterms = self._techterm.extract_from_pdf(pdf_candidates, ranking)

        return techterms

    def _run_multi_domain_method(
        self,
        domain: str,
        pdf_path: str,
        multi_domain_pdfs: List[DomainPDFList],
    ) -> PDFTechnicalTermList:
        if not isinstance(self._method, BaseMultiDomainRankingMethod):
            raise RuntimeError("unreachable statement")

        domain_pdfs = next(
            filter(lambda pdfs: pdfs.domain == domain, multi_domain_pdfs),
            None,
        )
        if domain_pdfs is None:
            raise ValueError(f"'multi_domain_pdfs' does not contain domain '{domain}'")

        if pdf_path not in domain_pdfs.pdf_paths:
            raise ValueError(f"domain_pdfs in '{domain}' does not contain '{pdf_path}'")

        domain_candidates_list: List[DomainCandidateTermList] = []
        for single_domain_pdfs in multi_domain_pdfs:
            domain_candidates = self._create_domain_candidates(single_domain_pdfs)
            domain_candidates_list.append(domain_candidates)

        domain_candidates = next(
            filter(lambda item: item.domain == domain, domain_candidates_list)
        )
        pdf_candidates = next(
            filter(lambda pdf: pdf.pdf_path == pdf_path, domain_candidates.pdfs)
        )
        ranking = self._method.rank_domain_terms(domain, domain_candidates_list)
        techterms = self._techterm.extract_from_pdf(pdf_candidates, ranking)

        return techterms

    def _create_domain_candidates(
        self, domain_pdfs: DomainPDFList
    ) -> DomainCandidateTermList:
        pdf_candidates_list: List[PDFCandidateTermList] = []

        for pdf_path in domain_pdfs.pdf_paths:
            pdfnxml = None
            if self._xml_config.use_cache:
                pdfnxml = self._cache.load_xml(pdf_path, self._xml_config)
            if pdfnxml is None:
                pdfnxml = self._xml.convert_as_content(pdf_path)
            if self._xml_config.use_cache:
                self._cache.store_xml(pdfnxml, self._xml_config)

            candidates = None
            if self._candidates_config.use_cache:
                candidates = self._cache.load_candidates(
                    pdf_path, self._candidates_config
                )
            if candidates is None:
                candidates = self._candidates.extract_from_xml_content(pdfnxml)
            if self._candidates_config.use_cache:
                self._cache.store_candidates(candidates, self._candidates_config)

            pdf_candidates_list.append(candidates)

        return DomainCandidateTermList(domain_pdfs.domain, pdf_candidates_list)
