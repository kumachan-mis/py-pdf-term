from typing import List, Optional

from py_pdf_term.techterms import PDFTechnicalTermList

from .caches import DEFAULT_CACHE_DIR
from .configs import (
    CandidateLayerConfig,
    MethodLayerConfig,
    StylingLayerConfig,
    TechnicalTermLayerConfig,
    XMLLayerConfig,
)
from .data import DomainPDFList
from .layers import (
    CandidateLayer,
    MethodLayer,
    StylingLayer,
    TechnicalTermLayer,
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
    XMLLayerCacheMapper,
)


class PyPDFTermExtractor:
    """Top level class of py-pdf-term. E2E class to extract terminologies from PDF file.

    Args:
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
            too long terms or wrongly concatenated terms. When XML Layer extracts a text
            from a table, figure or something in a PDF file, texts in them are often
            wrongly concatenated so that the text looks like one too long candidate
            term. This is used in Candidate Term Layer.
            e.g. If a PDF have a table to compare sort algorithms and the header text
            wanna mean "Selection Sort" | "Quick Sort" | "Merge Sort", the text is
            recognized as a word like "Selection Sort Quick Sort Merge Sort". This
            wrongly concatenated word must be split down into three algorithm names.

        augmenter_mapper:
            Mapper from an element in `candidate_config.augmenters` to a class to
            augment candidates. The augumentation means that if a long candidate term is
            found, sub-terms of the original term could also be candidates. This is used
            in Candidate Term Layer.
            e.g. Original long term: "Structure of Layered Architecture". Augmented sub-
            terms: "Structure" and "Layered Architecture".

        single_method_mapper:
            Mapper from `method_config.method` to a class to calculate method scores of
            candidate terms when `method_config.method_type` equals to "single".
            A single-domain ranking method is an ranking algorithm which can calculate
            method scores without cross-domain information.
            e.g. Term-Frequency algorithm uses only frequency of occurcences of terms.
            Therefore, TF is a single-domain ranking method.

        multi_method_mapper:
            Mapper from `method_config.method` to a class to calculate method scores of
            candidate terms when `method_config.method_type` equals to "multi".
            A multi-domain ranking method is an ranking algorithm which calculate method
            scores with cross-domain information.
            e.g. TF-IDF algorithm uses Inverse Document Frequency, which goes to high
            then a term appears frequently in a target domain but not in the other
            domains. To find IDF score, cross-domain data are required. Therefore,
            TF-IDF is a multi-domain ranking method.

        styling_score_mapper:
            Mapper from an element in `styling_config.styling_scores` to a class to
            calculate styling scores of candidate terms. Each scoring class is expected
            to focus one specific styling feature. Then different types of scores are
            combined later.

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
            local dirctory, a url or a bucket name of a cloud storage service.
    """

    def __init__(
        self,
        xml_config: Optional[XMLLayerConfig] = None,
        candidate_config: Optional[CandidateLayerConfig] = None,
        method_config: Optional[MethodLayerConfig] = None,
        styling_config: Optional[StylingLayerConfig] = None,
        techterm_config: Optional[TechnicalTermLayerConfig] = None,
        bin_opener_mapper: Optional[BinaryOpenerMapper] = None,
        lang_tokenizer_mapper: Optional[LanguageTokenizerMapper] = None,
        token_filter_mapper: Optional[CandidateTokenFilterMapper] = None,
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
            token_filter_mapper=token_filter_mapper,
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
        """Function to extract terminologies from PDF file.

        Args:
            domain:
                Domain name which the input PDF file belongs to. This may be the name of
                a course, the name of a technical field or something.

            pdf_path:
                Path like string to the input PDF file which terminologies to be
                extracted. The file MUST belong to `domain`.

            single_domain_pdfs:
                List of path like strings to the PDF files which belong to `domain`.
                `single_domain_pdfs.domain` MUST equals to `domain`. This argument is
                required when a single-domain ranking method is to be used.

            multi_domain_pdfs:
                List of path like strings to the PDF files which classified by domain.
                There MUST be an element in `multi_domain_pdfs` whose domain equals to
                `domain`. This argument is required when a multi-domain ranking method
                is to be used.

        Returns:
            PDFTechnicalTermList:
                Terminology list per page from the input PDF file.
        """
        pdf_techterms = self._techterm_layer.create_pdf_techterms(
            domain, pdf_path, single_domain_pdfs, multi_domain_pdfs
        )
        return pdf_techterms
