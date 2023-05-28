from py_pdf_term.stylings import PDFStylingScoreList, StylingScorer

from ..caches import DEFAULT_CACHE_DIR
from ..configs import StylingLayerConfig
from ..mappers import StylingLayerCacheMapper, StylingScoreMapper
from .candidate import CandidateLayer


class StylingLayer:
    """Layer to calclate styling scores from a PDF file using candidate layer.

    Args
    ----
        candidate_layer:
            Layer to extract candidate terms.
        config:
            Configuration for this layer. If None, the default configuration is used.
        styling_score_mapper:
            Mapper to find styling score classes from configuration. If None, the
            default mapper is used.
        cache_mapper:
            Mapper to find cache class from configuration. If None, the default mapper
            is used.

    """

    def __init__(
        self,
        candidate_layer: CandidateLayer,
        config: StylingLayerConfig | None = None,
        styling_score_mapper: StylingScoreMapper | None = None,
        cache_mapper: StylingLayerCacheMapper | None = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ) -> None:
        if config is None:
            config = StylingLayerConfig()
        if styling_score_mapper is None:
            styling_score_mapper = StylingScoreMapper.default_mapper()
        if cache_mapper is None:
            cache_mapper = StylingLayerCacheMapper.default_mapper()

        styling_score_clses = styling_score_mapper.bulk_find(config.styling_scores)
        cache_cls = cache_mapper.find(config.cache)

        self._scorer = StylingScorer(styling_score_clses=styling_score_clses)
        self._cache = cache_cls(cache_dir=cache_dir)
        self._config = config

        self._candidate_layer = candidate_layer

    def create_pdf_styling_scores(self, pdf_path: str) -> PDFStylingScoreList:
        """Create style score list from a PDF file.

        Args
        ----
            pdf_path:
                PDF file path to calculate styling scores.

        Returns
        -------
            PDFStylingScoreList:
                List of styling scores for each page in the PDF file.
        """

        styling_scores = self._cache.load(pdf_path, self._config)

        if styling_scores is None:
            pdf_candidates = self._candidate_layer.create_pdf_candidates(pdf_path)
            styling_scores = self._scorer.score_pdf_candidates(pdf_candidates)

        self._cache.store(styling_scores, self._config)

        return styling_scores

    def remove_cache(self, pdf_path: str) -> None:
        """Remove a cache file for a PDF file.

        Args
        ----
            pdf_path:
                PDF file path to remove a cache file.
        """

        self._cache.remove(pdf_path, self._config)
