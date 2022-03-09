from abc import ABCMeta, abstractmethod
from typing import List, Optional

from py_pdf_term._common.data import Term
from ..classifiers import (
    BaseTokenClassifier,
    EnglishTokenClassifier,
    JapaneseTokenClassifier,
)


class BaseSplitter(metaclass=ABCMeta):
    def __init__(self, classifiers: Optional[List[BaseTokenClassifier]] = None) -> None:
        if classifiers is None:
            classifiers = [
                JapaneseTokenClassifier(),
                EnglishTokenClassifier(),
            ]

        self._classifiers = classifiers

    @abstractmethod
    def split(self, term: Term) -> List[Term]:
        raise NotImplementedError(f"{self.__class__.__name__}.split()")
