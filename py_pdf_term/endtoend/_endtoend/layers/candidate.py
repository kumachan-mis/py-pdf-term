from typing import List, Optional

from py_pdf_term.candidates import (
    CandidateTermExtractor,
    DomainCandidateTermList,
    PDFCandidateTermList,
)

from ..caches import DEFAULT_CACHE_DIR
from ..configs import CandidateLayerConfig
from ..data import DomainPDFList
from ..mappers import (
    AugmenterMapper,
    CandidateLayerCacheMapper,
    CandidateTermFilterMapper,
    CandidateTokenFilterMapper,
    LanguageTokenizerMapper,
    SplitterMapper,
)
from .xml import XMLLayer


class CandidateLayer:
    def __init__(
        self,
        xml_layer: XMLLayer,
        config: Optional[CandidateLayerConfig] = None,
        lang_tokenizer_mapper: Optional[LanguageTokenizerMapper] = None,
        token_filter_mapper: Optional[CandidateTokenFilterMapper] = None,
        term_filter_mapper: Optional[CandidateTermFilterMapper] = None,
        splitter_mapper: Optional[SplitterMapper] = None,
        augmenter_mapper: Optional[AugmenterMapper] = None,
        cache_mapper: Optional[CandidateLayerCacheMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ) -> None:
        if config is None:
            config = CandidateLayerConfig()
        if lang_tokenizer_mapper is None:
            lang_tokenizer_mapper = LanguageTokenizerMapper.default_mapper()
        if token_filter_mapper is None:
            token_filter_mapper = CandidateTokenFilterMapper.default_mapper()
        if term_filter_mapper is None:
            term_filter_mapper = CandidateTermFilterMapper.default_mapper()
        if splitter_mapper is None:
            splitter_mapper = SplitterMapper.default_mapper()
        if augmenter_mapper is None:
            augmenter_mapper = AugmenterMapper.default_mapper()
        if cache_mapper is None:
            cache_mapper = CandidateLayerCacheMapper.default_mapper()

        lang_tokenizer_clses = lang_tokenizer_mapper.bulk_find(config.lang_tokenizers)
        token_filter_clses = token_filter_mapper.bulk_find(config.token_filters)
        term_filter_clses = term_filter_mapper.bulk_find(config.term_filters)
        splitter_clses = splitter_mapper.bulk_find(config.splitters)
        augmenter_clses = augmenter_mapper.bulk_find(config.augmenters)
        cache_cls = cache_mapper.find(config.cache)

        self._extractor = CandidateTermExtractor(
            lang_tokenizer_clses=lang_tokenizer_clses,
            token_filter_clses=token_filter_clses,
            term_filter_clses=term_filter_clses,
            splitter_clses=splitter_clses,
            augmenter_clses=augmenter_clses,
        )
        self._cache = cache_cls(cache_dir=cache_dir)
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
        pdf_candidates = self._cache.load(pdf_path, self._config)

        if pdf_candidates is None:
            pdfnxml = self._xml_layer.create_pdfnxml(pdf_path)
            pdf_candidates = self._extractor.extract_from_xml_element(pdfnxml)

        self._cache.store(pdf_candidates, self._config)

        return pdf_candidates

    def remove_cache(self, pdf_path: str) -> None:
        self._cache.remove(pdf_path, self._config)
