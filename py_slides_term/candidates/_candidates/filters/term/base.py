import re
from abc import ABCMeta, abstractmethod

from py_slides_term._common.data import Term
from py_slides_term._common.consts import JAPANESE_REGEX, ENGLISH_REGEX, NUMBER_REGEX


class BaseCandidateTermFilter(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def inscope(self, term: Term) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.inscope()")

    @abstractmethod
    def is_candidate(self, scoped_term: Term) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.is_candidate()")


class BaseJapaneseCandidateTermFilter(BaseCandidateTermFilter):
    def inscope(self, term: Term) -> bool:
        regex = re.compile(rf"({ENGLISH_REGEX}|{JAPANESE_REGEX}|{NUMBER_REGEX}|\s|\-)+")
        return term.lang == "ja" and regex.fullmatch(str(term)) is not None


class BaseEnglishCandidateTermFilter(BaseCandidateTermFilter):
    def inscope(self, term: Term) -> bool:
        regex = re.compile(rf"({ENGLISH_REGEX}|{NUMBER_REGEX}|\s|\-)+")
        return term.lang == "en" and regex.fullmatch(str(term)) is not None