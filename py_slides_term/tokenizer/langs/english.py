import re
from .base import BaseLanguageTokenizer
from typing import List, Any

import en_core_web_sm

from ..data import Morpheme
from py_slides_term.share.consts import ALPHABET_REGEX, SYMBOL_REGEX


class EnglishTokenizer(BaseLanguageTokenizer):
    # public
    def __init__(self):
        # pyright:reportUnknownMemberType=false
        self._en_model = en_core_web_sm.load()
        self._en_model.disable_pipes("parser", "ner", "lemmatizer")

        self._en_regex = re.compile(ALPHABET_REGEX)
        self._symbol_regex = re.compile(SYMBOL_REGEX)

    def inscope(self, text: str) -> bool:
        return self._en_regex.search(text) is not None

    def tokenize(self, text: str) -> List[Morpheme]:
        # pyright:reportUnknownArgumentType=false
        # pyright:reportUnknownLambdaType=false
        return list(
            filter(
                lambda morpheme: morpheme.pos not in {"SPACE"},
                map(lambda token: self._create_morpheme(token), self._en_model(text)),
            )
        )

    # private
    def _create_morpheme(self, token: Any) -> Morpheme:
        if self._symbol_regex.fullmatch(token.text):
            return Morpheme(
                "en", token.text, "SYM", "*", "*", "*", "SYM", token.text, False
            )

        return Morpheme(
            "en",
            token.text,
            token.pos_,
            token.tag_,
            "*",
            "*",
            token.pos_,
            token.shape_,
            token.is_stop,
        )
