from typing import List, Optional

from .data import Morpheme
from .langs import (
    BaseLanguageTokenizer,
    JapaneseTokenizer,
    EnglishTokenizer,
)


class Tokenizer:
    def __init__(
        self, lang_tokenizers: Optional[List[BaseLanguageTokenizer]] = None
    ) -> None:
        if lang_tokenizers is None:
            lang_tokenizers = [JapaneseTokenizer(), EnglishTokenizer()]

        self._lang_tokenizers = lang_tokenizers

    def tokenize(self, text: str) -> List[Morpheme]:
        if not text:
            return []

        for tokenizer in self._lang_tokenizers:
            if tokenizer.inscope(text):
                return tokenizer.tokenize(text)

        return []
