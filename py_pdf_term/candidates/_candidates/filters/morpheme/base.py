from abc import ABCMeta, abstractmethod
from typing import List

from py_pdf_term.tokenizer import Morpheme


class BaseCandidateMorphemeFilter(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def inscope(self, morpheme: Morpheme) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.inscope()")

    @abstractmethod
    def is_partof_candidate(self, morphemes: List[Morpheme], idx: int) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.is_partof_candidate()")
