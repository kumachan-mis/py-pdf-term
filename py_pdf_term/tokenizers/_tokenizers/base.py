from abc import ABCMeta, abstractmethod

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
                Text to test.

        Returns
        -------
            bool:
                True if the text is in the scope of the language tokenizer, otherwise
                False.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.inscope()")

    @abstractmethod
    def tokenize(self, scoped_text: str) -> list[Token]:
        """Tokenize a scoped text into a list of tokens.

        Args
        ----
            scoped_text:
                Text to tokenize. This text is expected to be in the scope of the
                language tokenizer.

        Returns
        -------
            list[Token]:
                List of tokens.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.tokenize()")

    @classmethod
    @abstractmethod
    def class_init(cls) -> None:
        """Initialize the language tokenizer class. This method is expected to be
        called before using the language tokenizer.
        """

        raise NotImplementedError(f"{cls.__name__}.class_init()")
