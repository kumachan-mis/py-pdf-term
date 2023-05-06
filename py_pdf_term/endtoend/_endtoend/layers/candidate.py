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
    TokenClassifierMapper,
)
from .xml import XMLLayer


class CandidateLayer:
    """A layer to extract candidate terms using XMLLayer.

    Args
    ----
        xml_layer:
            a layer to create textful XML elements from a PDF file.
        config:
            a configuration for this layer. If None, the default configuration is used.
        lang_tokenizer_mapper:
            a mapper to find language tokenizer classes from configuration. If None, the
            default mapper is used.
        token_classifier_mapper:
            a mapper to find token classifier classes from configuration. If None, the
            default mapper is used.
        token_filter_mapper:
            a mapper to find token filter classes from configuration. If None, the
            default mapper is used.
        term_filter_mapper:
            a mapper to find term filter classes from configuration. If None, the
            default mapper is used.
        splitter_mapper:
            a mapper to find splitter classes from configuration. If None, the default
            mapper is used.
        augmenter_mapper:
            a mapper to find augmenter classes from configuration. If None, the default
            mapper is used.
        cache_mapper:
            a mapper to find cache class from configuration. If None, the default mapper
            is used.
        cache_dir:
            a directory path to store cache files. If None, the default directory is
            used.
    """

    def __init__(
        self,
        xml_layer: XMLLayer,
        config: Optional[CandidateLayerConfig] = None,
        lang_tokenizer_mapper: Optional[LanguageTokenizerMapper] = None,
        token_classifier_mapper: Optional[TokenClassifierMapper] = None,
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
        if token_classifier_mapper is None:
            token_classifier_mapper = TokenClassifierMapper.default_mapper()
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
        classifier_clses = token_classifier_mapper.bulk_find(config.token_classifiers)
        token_filter_clses = token_filter_mapper.bulk_find(config.token_filters)
        term_filter_clses = term_filter_mapper.bulk_find(config.term_filters)
        splitter_clses = splitter_mapper.bulk_find(config.splitters)
        augmenter_clses = augmenter_mapper.bulk_find(config.augmenters)
        cache_cls = cache_mapper.find(config.cache)

        self._extractor = CandidateTermExtractor(
            lang_tokenizer_clses=lang_tokenizer_clses,
            token_classifier_clses=classifier_clses,
            token_filter_clses=token_filter_clses,
            term_filter_clses=term_filter_clses,
            splitter_clses=splitter_clses,
            augmenter_clses=augmenter_clses,
        )
        self._cache = cache_cls(cache_dir=cache_dir)
        self._config = config

        self._xml_layer = xml_layer

    def create_domain_candidates(
        self, domain_pdfs: DomainPDFList
    ) -> DomainCandidateTermList:
        """Create candidate term list from a list of PDF files in a domain.

        Args
        ----
            domain_pdfs:
                a list of PDF files in a domain.

        Returns
        -------
            DomainCandidateTermList:
                a list of candidate terms in a domain.
        """

        pdf_candidates_list: List[PDFCandidateTermList] = []
        for pdf_path in domain_pdfs.pdf_paths:
            pdf_candidates = self.create_pdf_candidates(pdf_path)
            pdf_candidates_list.append(pdf_candidates)

        return DomainCandidateTermList(domain_pdfs.domain, pdf_candidates_list)

    def create_pdf_candidates(self, pdf_path: str) -> PDFCandidateTermList:
        """Create candidate term list from a PDF file.

        Args
        ----
            pdf_path:
                a path to a PDF file.

        Returns
        -------
            PDFCandidateTermList:
                a list of candidate terms in a PDF file.
        """

        pdf_candidates = self._cache.load(pdf_path, self._config)

        if pdf_candidates is None:
            pdfnxml = self._xml_layer.create_pdfnxml(pdf_path)
            pdf_candidates = self._extractor.extract_from_xml_element(pdfnxml)

        self._cache.store(pdf_candidates, self._config)

        return pdf_candidates

    def remove_cache(self, pdf_path: str) -> None:
        """Remove a cache file for a PDF file.

        Args
        ----
            pdf_path:
                a path to a PDF file to remove a cache file.
        """

        self._cache.remove(pdf_path, self._config)
