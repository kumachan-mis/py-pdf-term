from abc import ABCMeta, abstractmethod
from typing import List

from py_slides_term.tokenizer import BaseMorpheme


class BaseCandidateMorphemeFilter(metaclass=ABCMeta):
    # public
    def __init__(self):
        pass

    @abstractmethod
    def inscope(self, morpheme: BaseMorpheme) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.inscope()")

    @abstractmethod
    def is_partof_candidate(self, morphemes: List[BaseMorpheme], idx: int) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.is_partof_candidate()")
