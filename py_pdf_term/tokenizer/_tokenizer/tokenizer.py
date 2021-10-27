from typing import List, Optional

from .data import Token
from .langs import BaseLanguageTokenizer, EnglishTokenizer, JapaneseTokenizer


class Tokenizer:
    def __init__(
        self, lang_tokenizers: Optional[List[BaseLanguageTokenizer]] = None
    ) -> None:
        if lang_tokenizers is None:
            lang_tokenizers = [JapaneseTokenizer(), EnglishTokenizer()]

        self._lang_tokenizers = lang_tokenizers

    def tokenize(self, text: str) -> List[Token]:
        if not text:
            return []

        for tokenizer in self._lang_tokenizers:
            if tokenizer.inscope(text):
                return tokenizer.tokenize(text)

        return []
