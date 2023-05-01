from abc import ABCMeta, abstractmethod
from typing import List

from py_pdf_term.tokenizers import Token


class BaseCandidateTokenFilter(metaclass=ABCMeta):
    """Base class for filters of tokens which can be part of a candidate term."""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def inscope(self, token: Token) -> bool:
        """Test if a token is in scope of this filter.

        Args
        ----
            token:
                A token to be tested.


        Returns
        -------
            bool:
                True if the token is in scope of this filter, False otherwise.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.inscope()")

    @abstractmethod
    def is_partof_candidate(self, tokens: List[Token], idx: int) -> bool:
        """Test if a token can be part of a candidate term.

        Args
        ----
            tokens:
                A list of tokens.
            idx:
                An index of the token to be tested.


        Returns
        -------
            bool:
                True if the token can be part of a candidate term, False otherwise.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.is_partof_candidate()")
