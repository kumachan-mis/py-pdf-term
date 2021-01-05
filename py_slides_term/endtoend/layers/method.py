from typing import Any, List, Literal, Optional

from ..caches import RankingMethodLayerCache, DEFAULT_CACHE_DIR
from ..configs import RankingMethodLayerConfig
from ..mappers import SingleDomainRankingMethodMapper, MultiDomainRankingMethodMapper
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.methods import (
    BaseSingleDomainRankingMethod,
    BaseMultiDomainRankingMethod,
    DomainTermRanking,
)


class RankingMethodLayer:
    # public
    def __init__(
        self,
        config: Optional[RankingMethodLayerConfig] = None,
        single_method_mapper: Optional[SingleDomainRankingMethodMapper] = None,
        multi_method_mapper: Optional[MultiDomainRankingMethodMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ):
        if config is None:
            config = RankingMethodLayerConfig()
        if single_method_mapper is None:
            single_method_mapper = SingleDomainRankingMethodMapper.default_mapper()
        if multi_method_mapper is None:
            multi_method_mapper = MultiDomainRankingMethodMapper.default_mapper()

        if config.method_type == "single":
            method = single_method_mapper.find(config.method)
            if method is None:
                raise ValueError(
                    "cannot find single-domain"
                    f" ranking method named '{config.method}'"
                )
        elif config.method_type == "multi":
            method = multi_method_mapper.find(config.method)
            if method is None:
                raise ValueError(
                    "cannot find multi-domain"
                    f" ranking method named '{config.method}'"
                )
        else:
            raise ValueError(f"unknown method type '{config.method_type}'")

        self._method = method(**config.hyper_params)
        self._cache = RankingMethodLayerCache[Any](cache_dir=cache_dir)
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

        ranking_data = None
        if self._config.use_cache:
            ranking_data = self._cache.load(
                domain, self._config, self._method.collect_data_from_json
            )
        if ranking_data is None:
            ranking_data = self._method.collect_data(single_domain_candidates)

        term_ranking = self._method.rank_terms(single_domain_candidates, ranking_data)
        return term_ranking

    def _run_multi_domain_method(
        self,
        domain: str,
        multi_domain_candidates: List[DomainCandidateTermList],
    ) -> DomainTermRanking:
        if not isinstance(self._method, BaseMultiDomainRankingMethod):
            raise RuntimeError("unreachable statement")

        domains = set(map(lambda item: item.domain, multi_domain_candidates))
        if domain not in domains:
            raise ValueError(
                f"'multi_domain_candidates' does not contain domain '{domain}'"
            )

        ranking_data_list: List[Any] = []
        for domain_candidates in multi_domain_candidates:
            ranking_data = None
            if self._config.use_cache:
                ranking_data = self._cache.load(
                    domain, self._config, self._method.collect_data_from_json
                )
            if ranking_data is None:
                ranking_data = self._method.collect_data(domain_candidates)

            ranking_data_list.append(ranking_data)

        term_ranking = self._method.rank_domain_terms(
            domain, multi_domain_candidates, ranking_data_list
        )
        return term_ranking
