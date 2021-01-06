from typing import List, Optional

from .xml import XMLLayer
from ..data import DomainPDFList
from ..caches import CandidateLayerCache, DEFAULT_CACHE_DIR
from ..configs import CandidateLayerConfig
from ..mappers import CandidateMorphemeFilterMapper, CandidateTermFilterMapper
from py_slides_term.candidates import (
    CandidateTermExtractor,
    BaseCandidateMorphemeFilter,
    BaseCandidateTermFilter,
    DomainCandidateTermList,
    PDFCandidateTermList,
)


class CandidateLayer:
    # public
    def __init__(
        self,
        xml_layer: XMLLayer,
        config: Optional[CandidateLayerConfig] = None,
        morpheme_filter_mapper: Optional[CandidateMorphemeFilterMapper] = None,
        term_filter_mapper: Optional[CandidateTermFilterMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ):
        if config is None:
            config = CandidateLayerConfig()
        if morpheme_filter_mapper is None:
            morpheme_filter_mapper = CandidateMorphemeFilterMapper.default_mapper()
        if term_filter_mapper is None:
            term_filter_mapper = CandidateTermFilterMapper.default_mapper()

        morpheme_filters: List[BaseCandidateMorphemeFilter] = []
        for filter_name in config.morpheme_filters:
            morpheme_filter_cls = morpheme_filter_mapper.find(filter_name)
            if morpheme_filter_cls is None:
                raise ValueError(f"cannot find morpheme filter named '{filter_name}'")
            morpheme_filters.append(morpheme_filter_cls())

        term_filters: List[BaseCandidateTermFilter] = []
        for filter_name in config.term_filters:
            term_filter_cls = term_filter_mapper.find(filter_name)
            if term_filter_cls is None:
                raise ValueError(f"cannot find term filter named '{filter_name}'")
            term_filters.append(term_filter_cls())

        self._extractor = CandidateTermExtractor(
            morpheme_filters=morpheme_filters,
            term_filters=term_filters,
            modifying_particle_augmentation=config.modifying_particle_augmentation,
        )
        self._cache = CandidateLayerCache(cache_dir=cache_dir)
        self._config = config

        self._xml_layer = xml_layer

    def create_domain_candiates(
        self, domain_pdfs: DomainPDFList
    ) -> DomainCandidateTermList:
        pdf_candidates_list: List[PDFCandidateTermList] = []
        for pdf_path in domain_pdfs.pdf_paths:
            pdf_candidates = self.create_pdf_candidates(pdf_path)
            pdf_candidates_list.append(pdf_candidates)

        return DomainCandidateTermList(domain_pdfs.domain, pdf_candidates_list)

    def create_pdf_candidates(self, pdf_path: str) -> PDFCandidateTermList:
        if self._config.use_cache:
            candidates = self._cache.load(pdf_path, self._config)
            if candidates is not None:
                if self._config.remove_lower_layer_cache_when_completed:
                    self._xml_layer.remove_cache(pdf_path)
                return candidates

        pdfnxml = self._xml_layer.create_pdfnxml(pdf_path)
        candidates = self._extractor.extract_from_xml_content(pdfnxml)

        if self._config.use_cache:
            self._cache.store(candidates, self._config)
            if self._config.remove_lower_layer_cache_when_completed:
                self._xml_layer.remove_cache(pdf_path)

        return candidates
