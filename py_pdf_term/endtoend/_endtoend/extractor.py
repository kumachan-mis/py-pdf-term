from py_pdf_term.techterms import PDFTechnicalTermList

from .caches import DEFAULT_CACHE_DIR
from .configs import (
    CandidateLayerConfig,
    MultiDomainMethodLayerConfig,
    SingleDomainMethodLayerConfig,
    StylingLayerConfig,
    TechnicalTermLayerConfig,
    XMLLayerConfig,
)
from .data import DomainPDFList
from .layers import (
    CandidateLayer,
    MultiDomainMethodLayer,
    MultiDomainTechnicalTermLayer,
    SingleDomainMethodLayer,
    SingleDomainTechnicalTermLayer,
    StylingLayer,
    XMLLayer,
)
from .mappers import (
    AugmenterMapper,
    BinaryOpenerMapper,
    CandidateLayerCacheMapper,
    CandidateTermFilterMapper,
    CandidateTokenFilterMapper,
    LanguageTokenizerMapper,
    MethodLayerDataCacheMapper,
    MethodLayerRankingCacheMapper,
    MultiDomainRankingMethodMapper,
    SingleDomainRankingMethodMapper,
    SplitterMapper,
    StylingLayerCacheMapper,
    StylingScoreMapper,
    TokenClassifierMapper,
    XMLLayerCacheMapper,
)


class PyPDFTermSingleDomainExtractor:
    """Top level class of py-pdf-term. This class extracts technical terms from a PDF
    file withoout cross-domain information.

    Args
    ----
        xml_config:
            Config of XML Layer.

        candidate_config:
            Config of Candidate Term Layer.

        method_config:
            Config of Method Layer.

        styling_config:
            Config of Styling Layer.

        techterm_config:
            Config of Technial Term Layer.

        bin_opener_mapper:
            Mapper from `xml_config.open_bin` to a function to open a input PDF file in
            the binary mode. This is used in XML Layer.

        lang_tokenizer_mapper:
            Mapper from an element in `candidate_config.lang_tokenizers` to a class to
            tokenize texts in a specific language with spaCy. This is used in Candidate
            Term Layer.

        token_classifier_mapper:
            Mapper from an element in `candidate_config.token_classifiers` to a class to
            classify tokens into True/False by several functions. This is used in
            Candidate Term Layer.

        token_filter_mapper:
            Mapper from an element in `candidate_config.token_filters` to a class to
            filter tokens which are likely to be parts of candidates. This is used in
            Candidate Term Layer.

        term_filter_mapper:
            Mapper from an element in `candidate_config.term_filters` to a class to
            filter terms which are likely to be candidates. This is used in Candidate
            Term Layer.

        splitter_mapper:
            Mapper from an element in `candidate_config.splitters` to a class to split
            too long terms or wrongly concatenated terms. This is used in Candidate Term
            Layer.

        augmenter_mapper:
            Mapper from an element in `candidate_config.augmenters` to a class to
            augment candidates. The augumentation means that if a long candidate is
            found, sub-terms of it could also be candidates. This is used in Candidate
            Term Layer.

        method_mapper:
            Mapper from `method_config.method` to a class to calculate method scores of
            candidate terms. This is used in Method Layer.

        styling_score_mapper:
            Mapper from an element in `styling_config.styling_scores` to a class to
            calculate scores of candidate terms based on their styling such as color,
            fontsize and so on. This is used in Styling Layer.

        xml_cache_mapper:
            Mapper from `xml_config.cache` to a class to provide XML Layer with the
            cache  mechanism. The xml cache manages XML files converted from input PDF
            files.

        candidate_cache_mapper:
            Mapper from `candidate_config.cache` to a class to provide Candidate Term
            Layer with the cache mechanism. The candidate cache manages lists of
            candidate terms.

        method_ranking_cache_mapper:
            Mapper from `method_config.ranking_cache` to a class to provide Method Layer
            with the cache mechanism. The method ranking cache manages candidate terms
            ordered by the method scores.

        method_data_cache_mapper:
            Mapper from `method_config.data_cache` to a class to provide Method Layer
            with the cache mechanism. The method data cache manages analysis data of the
            candidate terms such as frequency or likelihood.

        styling_cache_mapper:
            Mapper from `styling_config.cache` to a class to provide Styling Layer with
            the cache mechanism. The styling cache manages candidate terms ordered by
            the styling scores.

        cache_dir:
            Path like string where cache files to be stored. For example, path to a
            local directory, a url or a bucket name of a cloud storage service.
    """

    def __init__(
        self,
        xml_config: XMLLayerConfig | None = None,
        candidate_config: CandidateLayerConfig | None = None,
        method_config: SingleDomainMethodLayerConfig | None = None,
        styling_config: StylingLayerConfig | None = None,
        techterm_config: TechnicalTermLayerConfig | None = None,
        bin_opener_mapper: BinaryOpenerMapper | None = None,
        lang_tokenizer_mapper: LanguageTokenizerMapper | None = None,
        token_classifier_mapper: TokenClassifierMapper | None = None,
        token_filter_mapper: CandidateTokenFilterMapper | None = None,
        term_filter_mapper: CandidateTermFilterMapper | None = None,
        splitter_mapper: SplitterMapper | None = None,
        augmenter_mapper: AugmenterMapper | None = None,
        method_mapper: SingleDomainRankingMethodMapper | None = None,
        styling_score_mapper: StylingScoreMapper | None = None,
        xml_cache_mapper: XMLLayerCacheMapper | None = None,
        candidate_cache_mapper: CandidateLayerCacheMapper | None = None,
        method_ranking_cache_mapper: MethodLayerRankingCacheMapper | None = None,
        method_data_cache_mapper: MethodLayerDataCacheMapper | None = None,
        styling_cache_mapper: StylingLayerCacheMapper | None = None,
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
            token_classifier_mapper=token_classifier_mapper,
            token_filter_mapper=token_filter_mapper,
            term_filter_mapper=term_filter_mapper,
            splitter_mapper=splitter_mapper,
            augmenter_mapper=augmenter_mapper,
            cache_mapper=candidate_cache_mapper,
            cache_dir=cache_dir,
        )
        method_layer = SingleDomainMethodLayer(
            candidate_layer=candidate_layer,
            config=method_config,
            method_mapper=method_mapper,
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
        techterm_layer = SingleDomainTechnicalTermLayer(
            candidate_layer=candidate_layer,
            method_layer=method_layer,
            styling_layer=styling_layer,
            config=techterm_config,
        )

        self._techterm_layer = techterm_layer

    def extract(
        self, pdf_path: str, domain_pdfs: DomainPDFList
    ) -> PDFTechnicalTermList:
        """Extract technical terms from a PDF file.

        Args
        ----
            pdf_path:
                Path like string to the input PDF file which terminologies to be
                extracted. The file MUST belong to `domain`.

            domain_pdfs:
                List of path like strings to the PDF files which belong to a specific
                domain.

        Returns:
            PDFTechnicalTermList:
                Terminology list per page from the input PDF file.
        """
        self._validate(pdf_path, domain_pdfs)

        pdf_techterms = self._techterm_layer.create_pdf_techterms(pdf_path, domain_pdfs)
        return pdf_techterms

    def _validate(self, pdf_path: str, domain_pdfs: DomainPDFList) -> None:
        DomainPDFList.validate(domain_pdfs)

        if pdf_path not in domain_pdfs.pdf_paths:
            raise ValueError(f"{pdf_path} must be included in domain_pdfs")


class PyPDFTermMultiDomainExtractor:
    """Top level class of py-pdf-term. This class extracts technical terms from a PDF
    file with cross-domain information.

    Args
    ----
        xml_config:
            Config of XML Layer.

        candidate_config:
            Config of Candidate Term Layer.

        method_config:
            Config of Method Layer.

        styling_config:
            Config of Styling Layer.

        techterm_config:
            Config of Technial Term Layer.

        bin_opener_mapper:
            Mapper from `xml_config.open_bin` to a function to open a input PDF file in
            the binary mode. This is used in XML Layer.

        lang_tokenizer_mapper:
            Mapper from an element in `candidate_config.lang_tokenizers` to a class to
            tokenize texts in a specific language with spaCy. This is used in Candidate
            Term Layer.

        token_classifier_mapper:
            Mapper from an element in `candidate_config.token_classifiers` to a class to
            classify tokens into True/False by several functions. This is used in
            Candidate Term Layer.

        token_filter_mapper:
            Mapper from an element in `candidate_config.token_filters` to a class to
            filter tokens which are likely to be parts of candidates. This is used in
            Candidate Term Layer.

        term_filter_mapper:
            Mapper from an element in `candidate_config.term_filters` to a class to
            filter terms which are likely to be candidates. This is used in Candidate
            Term Layer.

        splitter_mapper:
            Mapper from an element in `candidate_config.splitters` to a class to split
            too long terms or wrongly concatenated terms. This is used in Candidate Term
            Layer.

        augmenter_mapper:
            Mapper from an element in `candidate_config.augmenters` to a class to
            augment candidates. The augumentation means that if a long candidate is
            found, sub-terms of it could also be candidates. This is used in Candidate
            Term Layer.

        method_mapper:
            Mapper from `method_config.method` to a class to calculate method scores of
            candidate terms. This is used in Method Layer.

        styling_score_mapper:
            Mapper from an element in `styling_config.styling_scores` to a class to
            calculate scores of candidate terms based on their styling such as color,
            fontsize and so on. This is used in Styling Layer.

        xml_cache_mapper:
            Mapper from `xml_config.cache` to a class to provide XML Layer with the
            cache  mechanism. The xml cache manages XML files converted from input PDF
            files.

        candidate_cache_mapper:
            Mapper from `candidate_config.cache` to a class to provide Candidate Term
            Layer with the cache mechanism. The candidate cache manages lists of
            candidate terms.

        method_ranking_cache_mapper:
            Mapper from `method_config.ranking_cache` to a class to provide Method Layer
            with the cache mechanism. The method ranking cache manages candidate terms
            ordered by the method scores.

        method_data_cache_mapper:
            Mapper from `method_config.data_cache` to a class to provide Method Layer
            with the cache mechanism. The method data cache manages analysis data of the
            candidate terms such as frequency or likelihood.

        styling_cache_mapper:
            Mapper from `styling_config.cache` to a class to provide Styling Layer with
            the cache mechanism. The styling cache manages candidate terms ordered by
            the styling scores.

        cache_dir:
            Path like string where cache files to be stored. For example, path to a
            local directory, a url or a bucket name of a cloud storage service.
    """

    def __init__(
        self,
        xml_config: XMLLayerConfig | None = None,
        candidate_config: CandidateLayerConfig | None = None,
        method_config: MultiDomainMethodLayerConfig | None = None,
        styling_config: StylingLayerConfig | None = None,
        techterm_config: TechnicalTermLayerConfig | None = None,
        bin_opener_mapper: BinaryOpenerMapper | None = None,
        lang_tokenizer_mapper: LanguageTokenizerMapper | None = None,
        token_classifier_mapper: TokenClassifierMapper | None = None,
        token_filter_mapper: CandidateTokenFilterMapper | None = None,
        term_filter_mapper: CandidateTermFilterMapper | None = None,
        splitter_mapper: SplitterMapper | None = None,
        augmenter_mapper: AugmenterMapper | None = None,
        method_mapper: MultiDomainRankingMethodMapper | None = None,
        styling_score_mapper: StylingScoreMapper | None = None,
        xml_cache_mapper: XMLLayerCacheMapper | None = None,
        candidate_cache_mapper: CandidateLayerCacheMapper | None = None,
        method_ranking_cache_mapper: MethodLayerRankingCacheMapper | None = None,
        method_data_cache_mapper: MethodLayerDataCacheMapper | None = None,
        styling_cache_mapper: StylingLayerCacheMapper | None = None,
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
            token_classifier_mapper=token_classifier_mapper,
            token_filter_mapper=token_filter_mapper,
            term_filter_mapper=term_filter_mapper,
            splitter_mapper=splitter_mapper,
            augmenter_mapper=augmenter_mapper,
            cache_mapper=candidate_cache_mapper,
            cache_dir=cache_dir,
        )
        method_layer = MultiDomainMethodLayer(
            candidate_layer=candidate_layer,
            config=method_config,
            method_mapper=method_mapper,
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
        techterm_layer = MultiDomainTechnicalTermLayer(
            candidate_layer=candidate_layer,
            method_layer=method_layer,
            styling_layer=styling_layer,
            config=techterm_config,
        )

        self._techterm_layer = techterm_layer

    def extract(
        self, domain: str, pdf_path: str, multi_domain_pdfs: list[DomainPDFList]
    ) -> PDFTechnicalTermList:
        """Extract technical terms from a PDF file.

        Args
        ----
            domain:
                Domain name which the input PDF file belongs to. This may be the name of
                a course, the name of a technical field or something.

            pdf_path:
                Path like string to the input PDF file which terminologies to be
                extracted. The file MUST belong to `domain`.

            multi_domain_pdfs:
                List of path like strings to the PDF files which classified by domain.
                There MUST be an element in `multi_domain_pdfs` whose domain equals to
                `domain`.

        Returns:
            PDFTechnicalTermList:
                Terminology list per page from the input PDF file.
        """
        self._validate(domain, pdf_path, multi_domain_pdfs)

        pdf_techterms = self._techterm_layer.create_pdf_techterms(
            domain, pdf_path, multi_domain_pdfs
        )
        return pdf_techterms

    def _validate(
        self, domain: str, pdf_path: str, multi_domain_pdfs: list[DomainPDFList]
    ) -> None:
        if domain == "":
            raise ValueError("domain name must not be empty")

        if len(multi_domain_pdfs) < 2:
            raise ValueError("multi_domain_pdfs must have at least two elements")

        for domain_pdfs in multi_domain_pdfs:
            DomainPDFList.validate(domain_pdfs)

        domain_set = set(map(lambda pdfs: pdfs.domain, multi_domain_pdfs))
        if len(domain_set) != len(multi_domain_pdfs):
            raise ValueError("multi_domain_pdfs must have unique domain names")

        if domain not in domain_set:
            raise ValueError(f"{domain} must be included in multi_domain_pdfs")

        domain_pdfs = next(
            filter(lambda pdfs: pdfs.domain == domain, multi_domain_pdfs)
        )
        if pdf_path not in domain_pdfs.pdf_paths:
            raise ValueError(f"{pdf_path} must be included in {domain}")
