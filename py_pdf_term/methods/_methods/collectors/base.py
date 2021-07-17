from abc import ABCMeta, abstractmethod
from typing import Generic

from ..rankingdata.base import RankingData
from py_pdf_term.candidates import DomainCandidateTermList


class BaseRankingDataCollector(Generic[RankingData], metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def collect(self, domain_candidates: DomainCandidateTermList) -> RankingData:
        raise NotImplementedError(f"{self.__class__.__name__}.collect()")
