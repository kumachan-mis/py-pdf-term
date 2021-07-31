# pyright:reportUnknownMemberType=false
# pyright:reportUnknownArgumentType=false
# pyright:reportUnknownLambdaType=false

import re
from typing import List, Any

import en_core_web_sm

from .base import BaseLanguageTokenizer
from ..data import Morpheme
from py_pdf_term._common.consts import ALPHABET_REGEX, SYMBOL_REGEX


class EnglishTokenizer(BaseLanguageTokenizer):
    def __init__(self) -> None:
        enable_pipes = ["tok2vec", "tagger", "attribute_ruler", "lemmatizer"]
        self._model = en_core_web_sm.load()
        self._model.select_pipes(enable=enable_pipes)

        self._en_regex = re.compile(ALPHABET_REGEX)
        self._symbol_regex = re.compile(SYMBOL_REGEX)

    def inscope(self, text: str) -> bool:
        return self._en_regex.search(text) is not None

    def tokenize(self, text: str) -> List[Morpheme]:
        return list(map(self._create_morpheme, self._model(text)))

    def _create_morpheme(self, token: Any) -> Morpheme:
        if self._symbol_regex.fullmatch(token.text):
            return Morpheme(
                "en",
                token.text,
                "SYM",
                "*",
                "*",
                "*",
                "SYM",
                token.text,
                token.text,
                False,
            )

        return Morpheme(
            "en",
            token.text,
            token.pos_,
            token.tag_,
            "*",
            "*",
            token.pos_,
            token.lemma_.lower(),
            token.shape_,
            token.is_stop,
        )


class EnglishMorphemeClassifier:
    def is_adposition(self, morpheme: Morpheme) -> bool:
        return morpheme.pos == "ADP"

    def is_symbol(self, morpheme: Morpheme) -> bool:
        return morpheme.pos == "SYM"

    def is_connector_symbol(self, morpheme: Morpheme) -> bool:
        return morpheme.surface_form == "-" and morpheme.pos == "SYM"

    def is_meaningless(self, morpheme: Morpheme) -> bool:
        return self.is_symbol(morpheme) or self.is_adposition(morpheme)
