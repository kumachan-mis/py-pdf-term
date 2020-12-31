from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from pdf_slides_term.candidates.data import DomainCandidateTermList

RankingData = TypeVar("RankingData")


class BaseRankingDataCollector(Generic[RankingData], metaclass=ABCMeta):
    # public
    def __init__(self):
        pass

    @abstractmethod
    def collect(self, domain_candidates: DomainCandidateTermList) -> RankingData:
        raise NotImplementedError(
            f"{self.__class__.__name__}.collect() is not implemented"
        )
