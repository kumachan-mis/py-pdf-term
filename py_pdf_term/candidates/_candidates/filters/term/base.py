import re
from abc import ABCMeta, abstractmethod

from py_pdf_term._common.consts import ENGLISH_REGEX, JAPANESE_REGEX, NUMBER_REGEX
from py_pdf_term.tokenizers import Term


class BaseCandidateTermFilter(metaclass=ABCMeta):
    """Base class for filters of candidate terms."""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def inscope(self, term: Term) -> bool:
        """Test if a term is in scope of this filter.

        Args
        ----
            term:
                Term to be tested.


        Returns
        -------
            bool:
                True if the term is in scope of this filter, False otherwise.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.inscope()")

    @abstractmethod
    def is_candidate(self, scoped_term: Term) -> bool:
        """Test if a scoped term is a candidate term.

        Args
        ----
            scoped_term:
                Scoped term to be tested.

        Returns
        -------
            bool:
                True if the scoped term is a candidate term, False otherwise.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.is_candidate()")


class BaseJapaneseCandidateTermFilter(BaseCandidateTermFilter):
    """Base class for filters of Japanese candidate terms."""

    def inscope(self, term: Term) -> bool:
        regex = re.compile(rf"({ENGLISH_REGEX}|{JAPANESE_REGEX}|{NUMBER_REGEX}|\s|\-)+")
        return term.lang == "ja" and regex.fullmatch(str(term)) is not None


class BaseEnglishCandidateTermFilter(BaseCandidateTermFilter):
    """Base class for filters of English candidate terms."""

    def inscope(self, term: Term) -> bool:
        regex = re.compile(rf"({ENGLISH_REGEX}|{NUMBER_REGEX}|\s|\-)+")
        return term.lang == "en" and regex.fullmatch(str(term)) is not None
