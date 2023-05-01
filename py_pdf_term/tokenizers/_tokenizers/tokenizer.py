from typing import List, Optional

from .base import BaseLanguageTokenizer
from .data import Token
from .english import EnglishTokenizer
from .japanese import JapaneseTokenizer


class Tokenizer:
    """A tokenizer for multiple languages. This tokenizer uses SpaCy.

    Args
    ----
        lang_tokenizers:
            A list of language tokenizers. The order of the language tokenizers is
            important. The first language tokenizer that returns True in inscope() is
            used. If None, this tokenizer uses the default language tokenizers. The
            default language tokenizers are JapaneseTokenizer and EnglishTokenizer.
    """

    def __init__(
        self, lang_tokenizers: Optional[List[BaseLanguageTokenizer]] = None
    ) -> None:
        if lang_tokenizers is None:
            lang_tokenizers = [JapaneseTokenizer(), EnglishTokenizer()]

        self._lang_tokenizers = lang_tokenizers

    def tokenize(self, text: str) -> List[Token]:
        """Tokenize text into tokens.

        Args
        ----
            text:
                A text to tokenize.

        Returns
        -------
            List[Token]:
                A list of tokens.
        """

        if not text:
            return []

        for tokenizer in self._lang_tokenizers:
            if tokenizer.inscope(text):
                return tokenizer.tokenize(text)

        return []
