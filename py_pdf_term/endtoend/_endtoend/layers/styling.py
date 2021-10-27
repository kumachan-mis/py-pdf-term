from typing import Optional

from py_pdf_term.stylings import PDFStylingScoreList, StylingScorer

from ..caches import DEFAULT_CACHE_DIR
from ..configs import StylingLayerConfig
from ..mappers import StylingLayerCacheMapper, StylingScoreMapper
from .candidate import CandidateLayer


class StylingLayer:
    def __init__(
        self,
        candidate_layer: CandidateLayer,
        config: Optional[StylingLayerConfig] = None,
        styling_score_mapper: Optional[StylingScoreMapper] = None,
        cache_mapper: Optional[StylingLayerCacheMapper] = None,
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
        styling_scores = self._cache.load(pdf_path, self._config)

        if styling_scores is None:
            pdf_candidates = self._candidate_layer.create_pdf_candidates(pdf_path)
            styling_scores = self._scorer.score_pdf_candidates(pdf_candidates)

        self._cache.store(styling_scores, self._config)

        return styling_scores

    def remove_cache(self, pdf_path: str) -> None:
        self._cache.remove(pdf_path, self._config)
