from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Generic, Iterator, List, Optional

from py_pdf_term.candidates import DomainCandidateTermList

from .collectors import BaseRankingDataCollector
from .data import MethodTermRanking
from .rankers import BaseMultiDomainRanker, BaseSingleDomainRanker
from .rankingdata.base import RankingData


class BaseSingleDomainRankingMethod(Generic[RankingData], metaclass=ABCMeta):
    """Base class for ranking methods with an algorithm which does not require
    cross-domain information.

    Args
    ----
        data_collector:
            A collector of metadata to rank candidate terms in domain-specific PDF
            documents.
        ranker:
            A ranker of candidate terms in PDF documents by an algorithm which does not
            require cross-domain information.
    """

    def __init__(
        self,
        data_collector: BaseRankingDataCollector[RankingData],
        ranker: BaseSingleDomainRanker[RankingData],
    ) -> None:
        self._data_collector = data_collector
        self._ranker = ranker

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data: Optional[RankingData] = None,
    ) -> MethodTermRanking:
        """Rank candidate terms in PDF documents in a domain.

        Args
        ----
            domain_candidates:
                A list of candidate terms in domain-specific PDF documents.
            ranking_data:
                Metadata to rank candidate terms in PDF documents. If this argument is
                not None, this method skips collecting metadata and uses this argument
                instead. The default is None.

        Returns
        -------
            MethodTermRanking:
                A ranking result of candidate terms in PDF documents.
        """

        if ranking_data is None:
            ranking_data = self._data_collector.collect(domain_candidates)
        term_ranking = self._ranker.rank_terms(domain_candidates, ranking_data)
        return term_ranking

    def collect_data(self, domain_candidates: DomainCandidateTermList) -> RankingData:
        """Collect metadata to rank candidate terms in PDF documents. This method is
        used to collect metadata before ranking candidate terms in PDF documents. The
        following two code snippets are equivalent:

        ```
        ranking_data = method.collect_data(domain_candidates)
        term_ranking = method.rank_terms(domain_candidates, ranking_data)
        ```

        and

        ```
        term_ranking = method.rank_terms(domain_candidates)
        ```

        This method is useful when you want to utilize cached metadata to rank candidate
        terms in PDF documents.

        Args
        ----
            domain_candidates:
                A list of candidate terms in domain-specific PDF documents.

        Returns
        -------
            RankingData:
                Metadata to rank candidate terms in PDF documents.

        """

        ranking_data = self._data_collector.collect(domain_candidates)
        return ranking_data

    @classmethod
    @abstractmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> RankingData:
        """Collect metadata to rank candidate terms in PDF documents from a dictionary.
        This method is used to load cached metadata.

        Args
        ----
            obj:
                A dictionary which contains metadata to rank candidate terms in PDF
                documents in a domain.

        Returns
        -------
            RankingData:
                Metadata to rank candidate terms in PDF documents.
        """

        raise NotImplementedError(f"{cls.__name__}.collect_data_from_dict()")


class BaseMultiDomainRankingMethod(Generic[RankingData], metaclass=ABCMeta):
    """Base class for ranking methods with an algorithm which requires cross-domain
    information.

    Args
    ----
        data_collector:
            A collector of metadata to rank candidate terms in domain-specific PDF
            documents.
        ranker:
            A ranker of candidate terms in PDF documents by an algorithm which requires
            cross-domain information.
    """

    def __init__(
        self,
        data_collector: BaseRankingDataCollector[RankingData],
        ranker: BaseMultiDomainRanker[RankingData],
    ) -> None:
        self._data_collector = data_collector
        self._ranker = ranker

    def rank_terms(
        self,
        domain_candidates_list: List[DomainCandidateTermList],
        ranking_data_list: Optional[List[RankingData]] = None,
    ) -> Iterator[MethodTermRanking]:
        """Rank candidate terms in PDF documents in multiple domains.

        Args
        ----
            domain_candidates_list:
                A list of candidate terms in domain-specific PDF documents.
            ranking_data_list:
                Metadata to rank candidate terms in PDF documents. If this argument is
                not None, this method skips collecting metadata and uses this argument
                instead. The default is None.

        Yields
        ------
            MethodTermRanking:
                A ranking result of candidate terms in PDF documents.
        """

        if ranking_data_list is None:
            ranking_data_list = list(
                map(self._data_collector.collect, domain_candidates_list)
            )

        for domain_candidates in domain_candidates_list:
            term_ranking = self._ranker.rank_terms(domain_candidates, ranking_data_list)
            yield term_ranking

    def rank_domain_terms(
        self,
        domain: str,
        domain_candidates_list: List[DomainCandidateTermList],
        ranking_data_list: Optional[List[RankingData]] = None,
    ) -> MethodTermRanking:
        """Rank candidate terms in PDF documents in a domain.

        Args
        ----
            domain:
                A domain to rank candidate terms in PDF documents.
            domain_candidates_list:
                A list of candidate terms in domain-specific PDF documents.
            ranking_data_list:
                Metadata to rank candidate terms in PDF documents. If this argument is
                not None, this method skips collecting metadata and uses this argument
                instead. The default is None.

        Returns
        -------
            MethodTermRanking:
                A ranking result of candidate terms in PDF documents.
        """

        domain_candidates = next(
            filter(lambda item: item.domain == domain, domain_candidates_list)
        )

        if ranking_data_list is None:
            ranking_data_list = list(
                map(self._data_collector.collect, domain_candidates_list)
            )

        term_ranking = self._ranker.rank_terms(domain_candidates, ranking_data_list)
        return term_ranking

    def collect_data(self, domain_candidates: DomainCandidateTermList) -> RankingData:
        """Collect metadata to rank candidate terms in PDF documents. This method is
        used to collect metadata before ranking candidate terms in PDF documents. The
        following two code snippets are equivalent:

        ```
        ranking_data_list = list(map(method.collect_data, domain_candidates_list))
        term_ranking = method.rank_terms(domain_candidates, ranking_data_list)
        ```

        and

        ```
        term_ranking = method.rank_terms(domain_candidates)
        ```

        This method is useful when you want to utilize cached metadata to rank candidate
        terms in PDF documents.

        Args
        ----
            domain_candidates:
                A list of candidate terms in domain-specific PDF documents.
        """

        ranking_data = self._data_collector.collect(domain_candidates)
        return ranking_data

    @classmethod
    @abstractmethod
    def collect_data_from_dict(cls, obj: Dict[str, Any]) -> RankingData:
        """Collect metadata to rank candidate terms in PDF documents from a dictionary.
        This method is used to load cached metadata.

        Args
        ----
            obj:
                A dictionary which contains metadata to rank candidate terms in PDF
                documents in a domain.

        Returns
        -------
            RankingData:
                Metadata to rank candidate terms in PDF documents.
        """

        raise NotImplementedError(f"{cls.__name__}.collect_data_from_dict()")
