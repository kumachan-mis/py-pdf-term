from abc import ABCMeta, abstractmethod
from typing import List

from .data import Token


class BaseLanguageTokenizer(metaclass=ABCMeta):
    """Base class for language tokenizers. A language tokenizer is expected to tokenize
    a text into a list of tokens by SpaCy.
    """

    @abstractmethod
    def inscope(self, text: str) -> bool:
        """Test whether the text is in the scope of the language tokenizer.

        Args
        ----
            text:
                A text to test.

        Returns
        -------
            bool:
                True if the text is in the scope of the language tokenizer, otherwise
                False.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.inscope()")

    @abstractmethod
    def tokenize(self, scoped_text: str) -> List[Token]:
        """Tokenize a scoped text into a list of tokens.

        Args
        ----
            scoped_text:
                A text to tokenize. This text is expected to be in the scope of the
                language tokenizer.

        Returns
        -------
            List[Token]:
                A list of tokens.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.tokenize()")
