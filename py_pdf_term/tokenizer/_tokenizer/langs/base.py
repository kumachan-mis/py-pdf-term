from abc import ABCMeta, abstractmethod
from typing import List

from ..data import Token


class BaseLanguageTokenizer(metaclass=ABCMeta):
    @abstractmethod
    def inscope(self, text: str) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.inscope()")

    @abstractmethod
    def tokenize(self, text: str) -> List[Token]:
        raise NotImplementedError(f"{self.__class__.__name__}.tokenize()")
