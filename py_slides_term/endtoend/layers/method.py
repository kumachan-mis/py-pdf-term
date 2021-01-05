from typing import Any, List, Literal, Optional

from ..caches import MethodLayerRankingCache, MethodLayerDataCache, DEFAULT_CACHE_DIR
from ..configs import MethodLayerConfig
from ..mappers import SingleDomainRankingMethodMapper, MultiDomainRankingMethodMapper
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.methods import (
    BaseSingleDomainRankingMethod,
    BaseMultiDomainRankingMethod,
    DomainTermRanking,
)


class MethodLayer:
    # public
    def __init__(
        self,
        config: Optional[MethodLayerConfig] = None,
        single_method_mapper: Optional[SingleDomainRankingMethodMapper] = None,
        multi_method_mapper: Optional[MultiDomainRankingMethodMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ):
        if config is None:
            config = MethodLayerConfig()
        if single_method_mapper is None:
            single_method_mapper = SingleDomainRankingMethodMapper.default_mapper()
        if multi_method_mapper is None:
            multi_method_mapper = MultiDomainRankingMethodMapper.default_mapper()

        if config.method_type == "single":
            method_cls = single_method_mapper.find(config.method)
            if method_cls is None:
                raise ValueError(
                    "cannot find single-domain"
                    f" ranking method named '{config.method}'"
                )
        elif config.method_type == "multi":
            method_cls = multi_method_mapper.find(config.method)
            if method_cls is None:
                raise ValueError(
                    "cannot find multi-domain"
                    f" ranking method named '{config.method}'"
                )
        else:
            raise ValueError(f"unknown method type '{config.method_type}'")

        self._method = method_cls(**config.hyper_params)
        self._ranking_cache = MethodLayerRankingCache(cache_dir=cache_dir)
        self._data_cache = MethodLayerDataCache[Any](cache_dir=cache_dir)
        self._config = config

    def process(
        self,
        domain: str,
        single_domain_candidates: Optional[DomainCandidateTermList] = None,
        multi_domain_candidates: Optional[List[DomainCandidateTermList]] = None,
    ) -> DomainTermRanking:
        # pyright:reportUnnecessaryIsInstance=false
        if isinstance(self._method, BaseSingleDomainRankingMethod):
            if single_domain_candidates is None:
                raise ValueError(
                    "'single_domain_candidates' is required"
                    "when using single-domain ranking method"
                )
            term_ranking = self._run_single_domain_method(
                domain, single_domain_candidates
            )
            return term_ranking
        elif isinstance(self._method, BaseMultiDomainRankingMethod):
            if multi_domain_candidates is None:
                raise ValueError(
                    "'multi_domain_candidates' is required"
                    " when using multi-domain ranking method"
                )
            term_ranking = self._run_multi_domain_method(
                domain, multi_domain_candidates
            )
            return term_ranking
        else:
            raise RuntimeError("unreachable statement")

    @property
    def method_type(self) -> Literal["single", "multi"]:
        return self._config.method_type

    # private
    def _run_single_domain_method(
        self,
        domain: str,
        single_domain_candidates: DomainCandidateTermList,
    ) -> DomainTermRanking:
        if not isinstance(self._method, BaseSingleDomainRankingMethod):
            raise RuntimeError("unreachable statement")

        if domain != single_domain_candidates.domain:
            raise ValueError(
                f"domain of 'single_domain_candidates is expected to be '{domain}'"
                f" but got '{single_domain_candidates.domain}'"
            )

        pdf_paths = list(map(lambda item: item.pdf_path, single_domain_candidates.pdfs))
        if self._config.use_cache:
            term_ranking = self._ranking_cache.load(pdf_paths, self._config)
            if term_ranking is not None:
                return term_ranking

        ranking_data = None
        cache_miss = False
        if self._config.use_cache:
            ranking_data = self._data_cache.load(
                pdf_paths, self._config, self._method.collect_data_from_json
            )
        if ranking_data is None:
            ranking_data = self._method.collect_data(single_domain_candidates)
            cache_miss = True
        if self._config.use_cache and cache_miss:
            self._data_cache.store(pdf_paths, ranking_data, self._config)

        term_ranking = self._method.rank_terms(single_domain_candidates, ranking_data)
        if self._config.use_cache:
            self._ranking_cache.store(pdf_paths, term_ranking, self._config)

        return term_ranking

    def _run_multi_domain_method(
        self,
        domain: str,
        multi_domain_candidates: List[DomainCandidateTermList],
    ) -> DomainTermRanking:
        if not isinstance(self._method, BaseMultiDomainRankingMethod):
            raise RuntimeError("unreachable statement")

        domain_candidates = next(
            filter(lambda item: item.domain == domain, multi_domain_candidates),
            None,
        )
        if domain_candidates is None:
            raise ValueError(
                f"'multi_domain_candidates' does not contain domain '{domain}'"
            )

        if self._config.use_cache:
            pdf_paths = list(map(lambda item: item.pdf_path, domain_candidates.pdfs))
            term_ranking = self._ranking_cache.load(pdf_paths, self._config)
            if term_ranking is not None:
                return term_ranking

        ranking_data_list: List[Any] = []
        for _domain_candidates in multi_domain_candidates:
            pdf_paths = list(map(lambda item: item.pdf_path, _domain_candidates.pdfs))
            ranking_data = None
            cache_miss = False
            if self._config.use_cache:
                ranking_data = self._data_cache.load(
                    pdf_paths,
                    self._config,
                    self._method.collect_data_from_json,
                )
            if ranking_data is None:
                ranking_data = self._method.collect_data(_domain_candidates)
                cache_miss = True
            if self._config.use_cache and cache_miss:
                self._data_cache.store(pdf_paths, ranking_data, self._config)

            ranking_data_list.append(ranking_data)

        term_ranking = self._method.rank_domain_terms(
            domain, multi_domain_candidates, ranking_data_list
        )

        pdf_paths = list(map(lambda item: item.pdf_path, domain_candidates.pdfs))
        if self._config.use_cache:
            self._ranking_cache.store(pdf_paths, term_ranking, self._config)
        return term_ranking
