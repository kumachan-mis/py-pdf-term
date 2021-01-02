from abc import ABCMeta, abstractmethod
from typing import List

from py_slides_term.mecab import BaseMeCabMorpheme


class BaseCandidateMorphemeFilter(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def inscope(self, morpheme: BaseMeCabMorpheme) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.inscope()")

    @abstractmethod
    def is_partof_candidate(self, morphemes: List[BaseMeCabMorpheme], idx: int) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.is_partof_candidate()")
