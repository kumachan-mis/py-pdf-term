from .base import BaseLanguageTokenizer
from .data import Token
from .english import EnglishTokenizer
from .japanese import JapaneseTokenizer


class Tokenizer:
    """Tokenizer for multiple languages. This tokenizer uses SpaCy.

    Args
    ----
        lang_tokenizers:
            List of language tokenizers. The order of the language tokenizers is
            important. The first language tokenizer that returns True in inscope() is
            used. If None, this tokenizer uses the default language tokenizers. The
            default language tokenizers are JapaneseTokenizer and EnglishTokenizer.
    """

    def __init__(
        self, lang_tokenizers: list[BaseLanguageTokenizer] | None = None
    ) -> None:
        if lang_tokenizers is None:
            lang_tokenizers = [JapaneseTokenizer(), EnglishTokenizer()]

        self._lang_tokenizers = lang_tokenizers

    def tokenize(self, text: str) -> list[Token]:
        """Tokenize text into tokens.

        Args
        ----
            text:
                Text to tokenize.

        Returns
        -------
            list[Token]:
                List of tokens.
        """

        if not text:
            return []

        for tokenizer in self._lang_tokenizers:
            if tokenizer.inscope(text):
                return tokenizer.tokenize(text)

        return []
