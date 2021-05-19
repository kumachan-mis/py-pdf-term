import re
from abc import ABCMeta, abstractmethod

from py_slides_term.share.data import Term
from py_slides_term.share.consts import JAPANESE_REGEX, ENGLISH_REGEX, NUMBER_REGEX


class BaseCandidateTermFilter(metaclass=ABCMeta):
    # public
    def __init__(self):
        pass

    @abstractmethod
    def inscope(self, term: Term) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.inscope()")

    @abstractmethod
    def is_candidate(self, scoped_term: Term) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.is_candidate()")


class BaseJapaneseCandidateTermFilter(BaseCandidateTermFilter):
    # public
    def inscope(self, term: Term) -> bool:
        regex = re.compile(rf"({ENGLISH_REGEX}|{JAPANESE_REGEX}|{NUMBER_REGEX}|\s|\-)+")
        is_japanese = all(map(lambda morpheme: morpheme.lang == "ja", term.morphemes))
        return regex.fullmatch(str(term)) is not None and is_japanese


class BaseEnglishCandidateTermFilter(BaseCandidateTermFilter):
    # public
    def inscope(self, term: Term) -> bool:
        regex = re.compile(rf"({ENGLISH_REGEX}|{NUMBER_REGEX}|\s|\-)+")
        is_english = all(map(lambda morpheme: morpheme.lang == "en", term.morphemes))
        return regex.fullmatch(str(term)) is not None and is_english
