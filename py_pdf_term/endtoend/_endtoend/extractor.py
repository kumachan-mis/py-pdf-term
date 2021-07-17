from typing import List, Optional

from .configs import (
    XMLLayerConfig,
    CandidateLayerConfig,
    MethodLayerConfig,
    StylingLayerConfig,
    TechnicalTermLayerConfig,
)
from .mappers import (
    BinaryOpenerMapper,
    LanguageTokenizerMapper,
    CandidateMorphemeFilterMapper,
    CandidateTermFilterMapper,
    SplitterMapper,
    AugmenterMapper,
    SingleDomainRankingMethodMapper,
    MultiDomainRankingMethodMapper,
    StylingScoreMapper,
    XMLLayerCacheMapper,
    CandidateLayerCacheMapper,
    MethodLayerRankingCacheMapper,
    MethodLayerDataCacheMapper,
    StylingLayerCacheMapper,
)
from .layers import (
    XMLLayer,
    CandidateLayer,
    MethodLayer,
    StylingLayer,
    TechnicalTermLayer,
)
from .caches import DEFAULT_CACHE_DIR
from .data import DomainPDFList
from py_pdf_term.techterms import PDFTechnicalTermList


class PyPDFTermExtractor:
    def __init__(
        self,
        xml_config: Optional[XMLLayerConfig] = None,
        candidate_config: Optional[CandidateLayerConfig] = None,
        method_config: Optional[MethodLayerConfig] = None,
        styling_config: Optional[StylingLayerConfig] = None,
        techterm_config: Optional[TechnicalTermLayerConfig] = None,
        bin_opener_mapper: Optional[BinaryOpenerMapper] = None,
        lang_tokenizer_mapper: Optional[LanguageTokenizerMapper] = None,
        morpheme_filter_mapper: Optional[CandidateMorphemeFilterMapper] = None,
        term_filter_mapper: Optional[CandidateTermFilterMapper] = None,
        splitter_mapper: Optional[SplitterMapper] = None,
        augmenter_mapper: Optional[AugmenterMapper] = None,
        single_method_mapper: Optional[SingleDomainRankingMethodMapper] = None,
        multi_method_mapper: Optional[MultiDomainRankingMethodMapper] = None,
        styling_score_mapper: Optional[StylingScoreMapper] = None,
        xml_cache_mapper: Optional[XMLLayerCacheMapper] = None,
        candidate_cache_mapper: Optional[CandidateLayerCacheMapper] = None,
        method_ranking_cache_mapper: Optional[MethodLayerRankingCacheMapper] = None,
        method_data_cache_mapper: Optional[MethodLayerDataCacheMapper] = None,
        styling_cache_mapper: Optional[StylingLayerCacheMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ) -> None:
        xml_layer = XMLLayer(
            config=xml_config,
            bin_opener_mapper=bin_opener_mapper,
            cache_mapper=xml_cache_mapper,
            cache_dir=cache_dir,
        )
        candidate_layer = CandidateLayer(
            xml_layer=xml_layer,
            config=candidate_config,
            lang_tokenizer_mapper=lang_tokenizer_mapper,
            morpheme_filter_mapper=morpheme_filter_mapper,
            term_filter_mapper=term_filter_mapper,
            splitter_mapper=splitter_mapper,
            augmenter_mapper=augmenter_mapper,
            cache_mapper=candidate_cache_mapper,
            cache_dir=cache_dir,
        )
        method_layer = MethodLayer(
            candidate_layer=candidate_layer,
            config=method_config,
            single_method_mapper=single_method_mapper,
            multi_method_mapper=multi_method_mapper,
            ranking_cache_mapper=method_ranking_cache_mapper,
            data_cache_mapper=method_data_cache_mapper,
            cache_dir=cache_dir,
        )
        styling_layer = StylingLayer(
            candidate_layer=candidate_layer,
            config=styling_config,
            styling_score_mapper=styling_score_mapper,
            cache_mapper=styling_cache_mapper,
            cache_dir=cache_dir,
        )
        techterm_layer = TechnicalTermLayer(
            candidate_layer=candidate_layer,
            method_layer=method_layer,
            styling_layer=styling_layer,
            config=techterm_config,
        )

        self._techterm_layer = techterm_layer

    def extract(
        self,
        domain: str,
        pdf_path: str,
        single_domain_pdfs: Optional[DomainPDFList] = None,
        multi_domain_pdfs: Optional[List[DomainPDFList]] = None,
    ) -> PDFTechnicalTermList:
        pdf_techterms = self._techterm_layer.create_pdf_techterms(
            domain, pdf_path, single_domain_pdfs, multi_domain_pdfs
        )
        return pdf_techterms
