from abc import ABCMeta
from typing import Any

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
    """Base class for method layers to calculate term ranking from candidate terms
    using candidate layer.

    Args
    ----
        candidate_layer:
            Layer to extract candidate terms.
        config:
            Configuration for this layer. If None, the default configuration is used.
        ranking_cache_mapper:
            Mapper to find ranking cache classes from configuration. If None, the
            default mapper is used.
        data_cache_mapper:
            Mapper to find data cache classes from configuration. If None, the default
            mapper is used.
        cache_dir:
            Directory path to store cache files. If None, the default directory is
            used.
    """

    def __init__(
        self,
        candidate_layer: CandidateLayer,
        config: BaseMethodLayerConfig,
        ranking_cache_mapper: MethodLayerRankingCacheMapper | None,
        data_cache_mapper: MethodLayerDataCacheMapper | None,
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

    def remove_cache(self, pdf_paths: list[str]) -> None:
        """Remove cache file for given PDF paths in a domain.

        Args
        ----
            pdf_paths:
                List of PDF paths in a domain to remove a cache file.
        """

        self._ranking_cache.remove(pdf_paths, self._config)
        self._data_cache.remove(pdf_paths, self._config)


class SingleDomainMethodLayer(BaseMethodLayer):
    """Method layer to calculate term ranking with an algorithm which does not require
    cross-domain information using candidate terms.

    Args
    ----
        candidate_layer:
            Layer to extract candidate terms.
        config:
            Configuration for this layer. If None, the default configuration is used.
        method_mapper:
            Mapper to find ranking method classes from configuration. If None, the
            default mapper is used.
        ranking_cache_mapper:
            Mapper to find ranking cache classes from configuration. If None, the
            default mapper is used.
        data_cache_mapper:
            Mapper to find data cache classes from configuration. If None, the default
            mapper is used.
        cache_dir:
            Directory path to store cache files. If None, the default directory is
            used.
    """

    def __init__(
        self,
        candidate_layer: CandidateLayer,
        config: SingleDomainMethodLayerConfig | None = None,
        method_mapper: SingleDomainRankingMethodMapper | None = None,
        ranking_cache_mapper: MethodLayerRankingCacheMapper | None = None,
        data_cache_mapper: MethodLayerDataCacheMapper | None = None,
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
        """Create term ranking from candidate terms in a domain.

        Args
        ----
            domain_pdfs:
                List of PDFs in a domain to extract term ranking.

        Returns
        -------
            MethodTermRanking:
                Term ranking costructed from candidate terms.
        """

        term_ranking = self._ranking_cache.load(domain_pdfs.pdf_paths, self._config)

        if term_ranking is None:
            candidates = self._candidate_layer.create_domain_candidates(domain_pdfs)
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
    """Method layer to calculate term ranking with an algorithm which requires
    cross-domain information using candidate terms.

    Args
    ----
        candidate_layer:
            Layer to extract candidate terms.
        config:
            Configuration for this layer. If None, the default configuration is used.
        method_mapper:
            Mapper to find ranking method classes from configuration. If None, the
            default mapper is used.
        ranking_cache_mapper:
            Mapper to find ranking cache classes from configuration. If None, the
            default mapper is used.
        data_cache_mapper:
            Mapper to find data cache classes from configuration. If None, the default
            mapper is used.
        cache_dir:
            Directory path to store cache files. If None, the default directory is
            used.
    """

    def __init__(
        self,
        candidate_layer: CandidateLayer,
        config: MultiDomainMethodLayerConfig | None = None,
        method_mapper: MultiDomainRankingMethodMapper | None = None,
        ranking_cache_mapper: MethodLayerRankingCacheMapper | None = None,
        data_cache_mapper: MethodLayerDataCacheMapper | None = None,
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
        multi_domain_pdfs: list[DomainPDFList],
    ) -> MethodTermRanking:
        """Create term ranking from candidate terms in a domain.

        Args
        ----
            domain:
                Domain to construct term ranking.
            multi_domain_pdfs:
                List of PDFs in each domain.

        Returns
        -------
            MethodTermRanking:
                Term ranking costructed from candidate terms in the given domain.
        """

        target_domain_pdfs = next(
            filter(lambda item: item.domain == domain, multi_domain_pdfs), None
        )
        if target_domain_pdfs is None:
            raise ValueError(f"'multi_domain_pdfs' does not contain domain '{domain}'")

        term_ranking = self._ranking_cache.load(
            target_domain_pdfs.pdf_paths, self._config
        )

        if term_ranking is None:
            domain_candidates_list: list[DomainCandidateTermList] = []
            ranking_data_list: list[Any] = []
            for domain_pdfs in multi_domain_pdfs:
                candidates = self._candidate_layer.create_domain_candidates(domain_pdfs)
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
