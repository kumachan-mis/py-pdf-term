from typing import List, Optional

from ..caches import CandidateLayerCache, DEFAULT_CACHE_DIR
from ..configs import CandidateLayerConfig
from ..mappers import CandidateMorphemeFilterMapper, CandidateTermFilterMapper
from py_slides_term.pdftoxml import PDFnXMLContent
from py_slides_term.candidates import (
    CandidateTermExtractor,
    BaseCandidateMorphemeFilter,
    BaseCandidateTermFilter,
    PDFCandidateTermList,
)


class CandidateLayer:
    # public
    def __init__(
        self,
        config: Optional[CandidateLayerConfig] = None,
        morheme_filter_mapper: Optional[CandidateMorphemeFilterMapper] = None,
        term_filter_mapper: Optional[CandidateTermFilterMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ):
        if config is None:
            config = CandidateLayerConfig()
        if morheme_filter_mapper is None:
            morheme_filter_mapper = CandidateMorphemeFilterMapper.default_mapper()
        if term_filter_mapper is None:
            term_filter_mapper = CandidateTermFilterMapper.default_mapper()

        morpheme_filters: List[BaseCandidateMorphemeFilter] = []
        for filter_name in config.morpheme_filters:
            morpheme_filter = morheme_filter_mapper.find(filter_name)
            if morpheme_filter is None:
                raise ValueError(f"cannot find morpheme filter named '{filter_name}'")
            morpheme_filters.append(morpheme_filter)

        term_filters: List[BaseCandidateTermFilter] = []
        for filter_name in config.term_filters:
            term_filter = term_filter_mapper.find(filter_name)
            if term_filter is None:
                raise ValueError(f"cannot find term filter named '{filter_name}'")
            term_filters.append(term_filter)

        self._extractor = CandidateTermExtractor(
            morpheme_filters=morpheme_filters,
            term_filters=term_filters,
            modifying_particle_augmentation=config.modifying_particle_augmentation,
        )
        self._cache = CandidateLayerCache(cache_dir=cache_dir)
        self._config = config

    def process(self, pdfnxml: PDFnXMLContent) -> PDFCandidateTermList:
        candidates = None
        if self._config.use_cache:
            candidates = self._cache.load(pdfnxml.pdf_path, self._config)
        if candidates is None:
            candidates = self._extractor.extract_from_xml_content(pdfnxml)
        if self._config.use_cache:
            self._cache.store(candidates, self._config)

        return candidates
