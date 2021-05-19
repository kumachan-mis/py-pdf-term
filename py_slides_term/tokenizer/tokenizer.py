from typing import List

from .data import Morpheme
from .langs import (
    BaseLanguageTokenizer,
    JapaneseTokenizer,
    EnglishTokenizer,
)


class Tokenizer:
    # public
    def __init__(self):
        self._lang_tokenizers: List[BaseLanguageTokenizer] = [
            JapaneseTokenizer(),
            EnglishTokenizer(),
        ]

    def tokenize(self, text: str) -> List[Morpheme]:
        if not text:
            return []

        for tokenizer in self._lang_tokenizers:
            if tokenizer.inscope(text):
                return tokenizer.tokenize(text)

        return []
