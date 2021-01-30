import re
from abc import ABCMeta, abstractmethod
from py_slides_term.share.data import Term
from py_slides_term.share.consts import HIRAGANA_REGEX, KATAKANA_REGEX, KANJI_REGEX


JAPANESE_REGEX = rf"({HIRAGANA_REGEX}|{KATAKANA_REGEX}|{KANJI_REGEX})"
ENGLISH_REGEX = r"[A-Za-z ]"


class BaseCandidateTermFilter(metaclass=ABCMeta):
    # public
    def __init__(self):
        pass

    @abstractmethod
    def inscope(self, term: Term) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.within_scope()")

    @abstractmethod
    def is_candidate(self, scoped_term: Term) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.is_part_of_candidate()")


class BaseJapaneseCandidateTermFilter(BaseCandidateTermFilter):
    # public
    def inscope(self, term: Term) -> bool:
        ja_regex = re.compile(rf"{JAPANESE_REGEX}+")
        ja_en_regex = re.compile(rf"({JAPANESE_REGEX}|{ENGLISH_REGEX}|\-)+")
        return ja_en_regex.fullmatch(str(term)) is not None and any(
            map(
                lambda morpheme: ja_regex.fullmatch(morpheme.pos) is not None,
                term.morphemes,
            )
        )


class BaseEnglishCandidateTermFilter(BaseCandidateTermFilter):
    # public
    def inscope(self, term: Term) -> bool:
        en_regex = re.compile(rf"({ENGLISH_REGEX}|\-)+")
        return en_regex.fullmatch(str(term)) is not None and all(
            map(
                lambda morpheme: en_regex.fullmatch(morpheme.pos) is not None,
                term.morphemes,
            )
        )
