from abc import ABCMeta, abstractmethod
from typing import Generic

from py_pdf_term.candidates import DomainCandidateTermList

from ..rankingdata.base import RankingData


class BaseRankingDataCollector(Generic[RankingData], metaclass=ABCMeta):
    """Base class for ranking data collectors. This class is used to collect metadata
    to rank candidate terms in domain-specific PDF documents.
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def collect(self, domain_candidates: DomainCandidateTermList) -> RankingData:
        """Collect metadata to rank candidate terms in domain-specific PDF documents.

        Args
        ----
            domain_candidates:
                A list of candidate terms in domain-specific PDF documents.

        Returns
        -------
            RankingData:
                Metadata to rank candidate terms in PDF documents.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.collect()")
