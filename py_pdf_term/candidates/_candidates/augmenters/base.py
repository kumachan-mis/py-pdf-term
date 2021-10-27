from abc import ABCMeta, abstractmethod
from typing import List

from py_pdf_term._common.data import Term


class BaseAugmenter(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def augment(self, term: Term) -> List[Term]:
        raise NotImplementedError(f"{self.__class__.__name__}.augment()")
