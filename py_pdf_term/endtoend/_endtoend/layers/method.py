from abc import ABCMeta
from typing import Any, List, Optional

from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.methods import MethodTermRanking

from ..caches import DEFAULT_CACHE_DIR
from ..configs import (
    BaseMethodLayerConfig,
    MultiDomainMethodLayerConfig,
    SingleDomainMethodLayerConfig,
)
from ..data import DomainPDFList
from ..mappers import (
    MethodLayerDataCacheMapper,
    MethodLayerRankingCacheMapper,
    MultiDomainRankingMethodMapper,
    SingleDomainRankingMethodMapper,
)
from .candidate import CandidateLayer


class BaseMethodLayer(metaclass=ABCMeta):
    def __init__(
        self,
        candidate_layer: CandidateLayer,
        config: BaseMethodLayerConfig,
        ranking_cache_mapper: Optional[MethodLayerRankingCacheMapper],
        data_cache_mapper: Optional[MethodLayerDataCacheMapper],
        cache_dir: str,
    ) -> None:
        if ranking_cache_mapper is None:
            ranking_cache_mapper = MethodLayerRankingCacheMapper.default_mapper()
        if data_cache_mapper is None:
            data_cache_mapper = MethodLayerDataCacheMapper.default_mapper()

        ranking_cache_cls = ranking_cache_mapper.find(config.ranking_cache)
        data_cache_cls = data_cache_mapper.find(config.data_cache)

        self._ranking_cache = ranking_cache_cls(cache_dir=cache_dir)
        self._data_cache = data_cache_cls(cache_dir=cache_dir)
        self._config = config

        self._candidate_layer = candidate_layer

    def remove_cache(self, pdf_paths: List[str]) -> None:
        self._ranking_cache.remove(pdf_paths, self._config)
        self._data_cache.remove(pdf_paths, self._config)


class SingleDomainMethodLayer(BaseMethodLayer):
    def __init__(
        self,
        candidate_layer: CandidateLayer,
        config: Optional[SingleDomainMethodLayerConfig] = None,
        method_mapper: Optional[SingleDomainRankingMethodMapper] = None,
        ranking_cache_mapper: Optional[MethodLayerRankingCacheMapper] = None,
        data_cache_mapper: Optional[MethodLayerDataCacheMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ) -> None:
        if config is None:
            config = SingleDomainMethodLayerConfig()
        if method_mapper is None:
            method_mapper = SingleDomainRankingMethodMapper.default_mapper()

        super().__init__(
            candidate_layer, config, ranking_cache_mapper, data_cache_mapper, cache_dir
        )

        method_cls = method_mapper.find(config.method)
        self._method = method_cls(**config.hyper_params)

    def create_term_ranking(self, domain_pdfs: DomainPDFList) -> MethodTermRanking:
        term_ranking = self._ranking_cache.load(domain_pdfs.pdf_paths, self._config)

        if term_ranking is None:
            candidates = self._candidate_layer.create_domain_candiates(domain_pdfs)
            ranking_data = self._create_ranking_data(domain_pdfs, candidates)
            term_ranking = self._method.rank_terms(candidates, ranking_data)

        self._ranking_cache.store(domain_pdfs.pdf_paths, term_ranking, self._config)

        return term_ranking

    def _create_ranking_data(
        self, domain_pdfs: DomainPDFList, domain_candidates: DomainCandidateTermList
    ) -> Any:
        ranking_data = self._data_cache.load(
            domain_pdfs.pdf_paths,
            self._config,
            self._method.collect_data_from_dict,
        )

        if ranking_data is None:
            ranking_data = self._method.collect_data(domain_candidates)

        self._data_cache.store(domain_pdfs.pdf_paths, ranking_data, self._config)

        return ranking_data


class MultiDomainMethodLayer(BaseMethodLayer):
    def __init__(
        self,
        candidate_layer: CandidateLayer,
        config: Optional[MultiDomainMethodLayerConfig] = None,
        method_mapper: Optional[MultiDomainRankingMethodMapper] = None,
        ranking_cache_mapper: Optional[MethodLayerRankingCacheMapper] = None,
        data_cache_mapper: Optional[MethodLayerDataCacheMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ) -> None:
        if config is None:
            config = MultiDomainMethodLayerConfig()
        if method_mapper is None:
            method_mapper = MultiDomainRankingMethodMapper.default_mapper()

        super().__init__(
            candidate_layer, config, ranking_cache_mapper, data_cache_mapper, cache_dir
        )

        method_cls = method_mapper.find(config.method)
        self._method = method_cls(**config.hyper_params)

    def create_term_ranking(
        self,
        domain: str,
        multi_domain_pdfs: List[DomainPDFList],
    ) -> MethodTermRanking:
        target_domain_pdfs = next(
            filter(lambda item: item.domain == domain, multi_domain_pdfs), None
        )
        if target_domain_pdfs is None:
            raise ValueError(f"'multi_domain_pdfs' does not contain domain '{domain}'")

        term_ranking = self._ranking_cache.load(
            target_domain_pdfs.pdf_paths, self._config
        )

        if term_ranking is None:
            domain_candidates_list: List[DomainCandidateTermList] = []
            ranking_data_list: List[Any] = []
            for domain_pdfs in multi_domain_pdfs:
                candidates = self._candidate_layer.create_domain_candiates(domain_pdfs)
                ranking_data = self._create_ranking_data(domain_pdfs, candidates)
                domain_candidates_list.append(candidates)
                ranking_data_list.append(ranking_data)

            term_ranking = self._method.rank_domain_terms(
                domain, domain_candidates_list, ranking_data_list
            )

        self._ranking_cache.store(
            target_domain_pdfs.pdf_paths, term_ranking, self._config
        )

        return term_ranking

    def _create_ranking_data(
        self, domain_pdfs: DomainPDFList, domain_candidates: DomainCandidateTermList
    ) -> Any:
        ranking_data = self._data_cache.load(
            domain_pdfs.pdf_paths,
            self._config,
            self._method.collect_data_from_dict,
        )

        if ranking_data is None:
            ranking_data = self._method.collect_data(domain_candidates)

        self._data_cache.store(domain_pdfs.pdf_paths, ranking_data, self._config)

        return ranking_data
