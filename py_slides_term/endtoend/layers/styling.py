from typing import Optional

from .candidate import CandidateLayer
from ..caches import DEFAULT_CACHE_DIR
from ..configs import StylingLayerConfig
from ..mappers import StylingLayerCacheMapper
from py_slides_term.stylings import StylingScorer, PDFStylingScoreList


class StylingLayer:
    # public
    def __init__(
        self,
        candidate_layer: CandidateLayer,
        config: Optional[StylingLayerConfig] = None,
        cache_mapper: Optional[StylingLayerCacheMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ):
        if config is None:
            config = StylingLayerConfig()
        if cache_mapper is None:
            cache_mapper = StylingLayerCacheMapper.default_mapper()

        cache_cls = cache_mapper.find(config.cache)

        self._scorer = StylingScorer()
        self._cache = cache_cls(cache_dir=cache_dir)
        self._config = config

        self._candidate_layer = candidate_layer

    def create_pdf_styling_scores(self, pdf_path: str) -> PDFStylingScoreList:
        styling_scores = self._cache.load(pdf_path, self._config)

        if styling_scores is None:
            pdf_candidates = self._candidate_layer.create_pdf_candidates(pdf_path)
            styling_scores = self._scorer.score_pdf_candidates(pdf_candidates)

        self._cache.store(styling_scores, self._config)

        if self._config.remove_lower_layer_cache:
            self._candidate_layer.remove_cache(pdf_path)

        return styling_scores

    def remove_cache(self, pdf_path: str):
        self._cache.remove(pdf_path, self._config)
