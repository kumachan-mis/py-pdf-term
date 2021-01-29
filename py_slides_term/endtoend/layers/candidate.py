from typing import List, Optional, Type

from .xml import XMLLayer
from ..data import DomainPDFList
from ..caches import CandidateLayerCache, DEFAULT_CACHE_DIR
from ..configs import CandidateLayerConfig
from ..mappers import (
    CandidateMorphemeFilterMapper,
    CandidateTermFilterMapper,
    SplitterMapper,
    AugmenterMapper,
)
from py_slides_term.candidates import (
    CandidateTermExtractor,
    BaseCandidateMorphemeFilter,
    BaseCandidateTermFilter,
    BaseSplitter,
    BaseAugmenter,
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
        splitter_mapper: Optional[SplitterMapper] = None,
        augmenter_mapper: Optional[AugmenterMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ):
        if config is None:
            config = CandidateLayerConfig()
        if morpheme_filter_mapper is None:
            morpheme_filter_mapper = CandidateMorphemeFilterMapper.default_mapper()
        if term_filter_mapper is None:
            term_filter_mapper = CandidateTermFilterMapper.default_mapper()
        if splitter_mapper is None:
            splitter_mapper = SplitterMapper.default_mapper()
        if augmenter_mapper is None:
            augmenter_mapper = AugmenterMapper.default_mapper()

        morpheme_filter_clses: List[Type[BaseCandidateMorphemeFilter]] = []
        for filter_name in config.morpheme_filters:
            morpheme_filter_cls = morpheme_filter_mapper.find(filter_name)
            if morpheme_filter_cls is None:
                raise ValueError(f"cannot find morpheme filter named '{filter_name}'")
            morpheme_filter_clses.append(morpheme_filter_cls)

        term_filter_clses: List[Type[BaseCandidateTermFilter]] = []
        for filter_name in config.term_filters:
            term_filter_cls = term_filter_mapper.find(filter_name)
            if term_filter_cls is None:
                raise ValueError(f"cannot find term filter named '{filter_name}'")
            term_filter_clses.append(term_filter_cls)

        splitter_clses: List[Type[BaseSplitter]] = []
        for splitter_name in config.splitters:
            splitter_cls = splitter_mapper.find(splitter_name)
            if splitter_cls is None:
                raise ValueError(f"cannot find splitter named '{splitter_name}'")
            splitter_clses.append(splitter_cls)

        augmenter_clses: List[Type[BaseAugmenter]] = []
        for augmenter_name in config.augmenters:
            augmenter_cls = augmenter_mapper.find(augmenter_name)
            if augmenter_cls is None:
                raise ValueError(f"cannot find augmenter named '{augmenter_name}'")
            augmenter_clses.append(augmenter_cls)

        self._extractor = CandidateTermExtractor(
            morpheme_filter_clses=morpheme_filter_clses,
            term_filter_clses=term_filter_clses,
            splitter_clses=splitter_clses,
            augmenter_clses=augmenter_clses,
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
                if self._config.remove_lower_layer_cache:
                    self._xml_layer.remove_cache(pdf_path)
                return candidates

        pdfnxml = self._xml_layer.create_pdfnxml(pdf_path)
        candidates = self._extractor.extract_from_xml_element(pdfnxml)

        if self._config.use_cache:
            self._cache.store(candidates, self._config)
            if self._config.remove_lower_layer_cache:
                self._xml_layer.remove_cache(pdf_path)

        return candidates
