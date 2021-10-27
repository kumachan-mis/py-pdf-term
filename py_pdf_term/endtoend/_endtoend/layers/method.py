from typing import Any, List, Optional

from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.methods import (
    BaseMultiDomainRankingMethod,
    BaseSingleDomainRankingMethod,
    MethodTermRanking,
)

from ..caches import DEFAULT_CACHE_DIR
from ..configs import MethodLayerConfig
from ..data import DomainPDFList
from ..mappers import (
    MethodLayerDataCacheMapper,
    MethodLayerRankingCacheMapper,
    MultiDomainRankingMethodMapper,
    SingleDomainRankingMethodMapper,
)
from .candidate import CandidateLayer


class MethodLayer:
    def __init__(
        self,
        candidate_layer: CandidateLayer,
        config: Optional[MethodLayerConfig] = None,
        single_method_mapper: Optional[SingleDomainRankingMethodMapper] = None,
        multi_method_mapper: Optional[MultiDomainRankingMethodMapper] = None,
        ranking_cache_mapper: Optional[MethodLayerRankingCacheMapper] = None,
        data_cache_mapper: Optional[MethodLayerDataCacheMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ) -> None:
        if config is None:
            config = MethodLayerConfig()
        if single_method_mapper is None:
            single_method_mapper = SingleDomainRankingMethodMapper.default_mapper()
        if multi_method_mapper is None:
            multi_method_mapper = MultiDomainRankingMethodMapper.default_mapper()
        if ranking_cache_mapper is None:
            ranking_cache_mapper = MethodLayerRankingCacheMapper.default_mapper()
        if data_cache_mapper is None:
            data_cache_mapper = MethodLayerDataCacheMapper.default_mapper()

        if config.method_type == "single":
            method_cls = single_method_mapper.find(config.method)
        elif config.method_type == "multi":
            method_cls = multi_method_mapper.find(config.method)
        else:
            raise ValueError(f"unknown method type '{config.method_type}'")

        ranking_cache_cls = ranking_cache_mapper.find(config.ranking_cache)
        data_cache_cls = data_cache_mapper.find(config.data_cache)

        self._method = method_cls(**config.hyper_params)
        self._ranking_cache = ranking_cache_cls(cache_dir=cache_dir)
        self._data_cache = data_cache_cls(cache_dir=cache_dir)
        self._config = config

        self._candidate_layer = candidate_layer

    # pyright:reportUnnecessaryIsInstance=false
    def create_term_ranking(
        self,
        domain: str,
        single_domain_pdfs: Optional[DomainPDFList] = None,
        multi_domain_pdfs: Optional[List[DomainPDFList]] = None,
    ) -> MethodTermRanking:

        if isinstance(self._method, BaseSingleDomainRankingMethod):
            if single_domain_pdfs is None:
                raise ValueError(
                    "'single_domain_pdfs' is required"
                    "when using single-domain ranking method"
                )
            term_ranking = self._run_single_domain_method(domain, single_domain_pdfs)
            return term_ranking

        elif isinstance(self._method, BaseMultiDomainRankingMethod):
            if multi_domain_pdfs is None:
                raise ValueError(
                    "'multi_domain_pdfs' is required"
                    " when using multi-domain ranking method"
                )
            term_ranking = self._run_multi_domain_method(domain, multi_domain_pdfs)
            return term_ranking

        else:
            raise RuntimeError("unreachable statement")

    def remove_cache(self, pdf_paths: List[str]) -> None:
        self._ranking_cache.remove(pdf_paths, self._config)
        self._data_cache.remove(pdf_paths, self._config)

    def _run_single_domain_method(
        self,
        domain: str,
        domain_pdfs: DomainPDFList,
    ) -> MethodTermRanking:
        if not isinstance(self._method, BaseSingleDomainRankingMethod):
            raise RuntimeError("unreachable statement")

        if domain != domain_pdfs.domain:
            raise ValueError(
                f"domain of 'single_domain_pdfs is expected to be '{domain}'"
                f" but got '{domain_pdfs.domain}'"
            )

        term_ranking = self._ranking_cache.load(domain_pdfs.pdf_paths, self._config)

        if term_ranking is None:
            candidates = self._candidate_layer.create_domain_candiates(domain_pdfs)
            ranking_data = self._create_ranking_data(domain_pdfs, candidates)
            term_ranking = self._method.rank_terms(candidates, ranking_data)

        self._ranking_cache.store(domain_pdfs.pdf_paths, term_ranking, self._config)

        return term_ranking

    def _run_multi_domain_method(
        self,
        domain: str,
        domain_pdfs_list: List[DomainPDFList],
    ) -> MethodTermRanking:
        if not isinstance(self._method, BaseMultiDomainRankingMethod):
            raise RuntimeError("unreachable statement")

        domain_pdfs = next(
            filter(lambda item: item.domain == domain, domain_pdfs_list), None
        )
        if domain_pdfs is None:
            raise ValueError(f"'multi_domain_pdfs' does not contain domain '{domain}'")

        term_ranking = self._ranking_cache.load(domain_pdfs.pdf_paths, self._config)

        if term_ranking is None:
            domain_candidates_list: List[DomainCandidateTermList] = []
            ranking_data_list: List[Any] = []
            for _domain_pdfs in domain_pdfs_list:
                candidates = self._candidate_layer.create_domain_candiates(_domain_pdfs)
                ranking_data = self._create_ranking_data(_domain_pdfs, candidates)
                domain_candidates_list.append(candidates)
                ranking_data_list.append(ranking_data)

            term_ranking = self._method.rank_domain_terms(
                domain, domain_candidates_list, ranking_data_list
            )

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
