from abc import ABCMeta, abstractmethod
from pdf_slides_term.mecab import BaseMeCabMorpheme


class BaseCandidateMorphemeFilter(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def inscope(self, morpheme: BaseMeCabMorpheme) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.within_scope()")

    @abstractmethod
    def is_partof_candidate(self, scoped_morpheme: BaseMeCabMorpheme) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.is_part_of_candidate()")
