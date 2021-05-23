from abc import ABCMeta, abstractmethod
from typing import List
from py_slides_term.share.data import Term


class BaseSplitter(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def split(self, term: Term) -> List[Term]:
        raise NotImplementedError(f"{self.__class__.__name__}.split()")
