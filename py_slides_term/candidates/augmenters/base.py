from abc import ABCMeta, abstractmethod
from typing import List
from py_slides_term.share.data import Term
from ..filters import FilterCombiner


class BaseAugmenter(metaclass=ABCMeta):
    # public
    def __init__(self, candidate_filter: FilterCombiner):
        pass

    @abstractmethod
    def augment(self, term: Term) -> List[Term]:
        raise NotImplementedError(f"{self.__class__.__name__}.augment()")
