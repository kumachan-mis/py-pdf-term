import re
from typing import Any

import en_core_web_sm

from py_pdf_term._common.consts import ALPHABET_REGEX, SYMBOL_REGEX

from .base import BaseLanguageTokenizer
from .data import Token


class EnglishTokenizer(BaseLanguageTokenizer):
    """Tokenizer for English. This tokenizer uses SpaCy's en_core_web_sm model."""

    def inscope(self, text: str) -> bool:
        return EnglishTokenizer._regex.search(text) is not None

    def tokenize(self, scoped_text: str) -> list[Token]:
        scoped_text = EnglishTokenizer._symbol_regex.sub(r" \1 ", scoped_text)
        return list(map(self._create_token, EnglishTokenizer._model(scoped_text)))

    def _create_token(self, token: Any) -> Token:
        if EnglishTokenizer._symbol_regex.fullmatch(token.text):
            return Token("en", token.text, "SYM", "*", "*", token.text)

        return Token(
            "en", token.text, token.pos_, token.tag_, "*", token.lemma_.lower()
        )

    @classmethod
    def class_init(cls) -> None:
        model = en_core_web_sm.load()  # pyright: ignore[reportUnknownMemberType]
        enable_pipes = ["tok2vec", "tagger", "attribute_ruler", "lemmatizer"]
        model.select_pipes(enable=enable_pipes)
        EnglishTokenizer._model = model

        EnglishTokenizer._regex = re.compile(ALPHABET_REGEX)
        EnglishTokenizer._symbol_regex = re.compile(rf"({SYMBOL_REGEX})")


EnglishTokenizer.class_init()
