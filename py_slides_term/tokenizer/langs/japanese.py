# pyright:reportUnknownMemberType=false
# pyright:reportUnknownArgumentType=false
# pyright:reportUnknownLambdaType=false

import re
from typing import List, Any

import ja_core_news_sm

from .base import BaseLanguageTokenizer
from ..data import Morpheme
from py_slides_term.share.consts import JAPANESE_REGEX, SYMBOL_REGEX, NOSPACE_REGEX

SPACES = re.compile(r"\s+")
GARBAGE_SPACE = re.compile(rf"(?<={NOSPACE_REGEX}) (?={NOSPACE_REGEX})")


class JapaneseTokenizer(BaseLanguageTokenizer):
    # public
    def __init__(self):
        self._model = ja_core_news_sm.load()
        self._model.select_pipes(
            disable=["tok2vec", "parser", "ner", "attribute_ruler"]
        )

        self._ja_regex = re.compile(JAPANESE_REGEX)
        self._symbol_regex = re.compile(SYMBOL_REGEX)

    def inscope(self, text: str) -> bool:
        return self._ja_regex.search(text) is not None

    def tokenize(self, text: str) -> List[Morpheme]:
        return list(map(self._create_morpheme, self._model(text)))

    # private
    def _create_morpheme(self, token: Any) -> Morpheme:
        if self._symbol_regex.fullmatch(token.text):
            return Morpheme(
                "ja", token.text, "補助記号", "一般", "*", "*", "SYM", token.text, False
            )

        pos_with_categories = token.tag_.split("-")
        num_categories = len(pos_with_categories) - 1

        pos = pos_with_categories[0]
        category = pos_with_categories[1] if num_categories >= 1 else "*"
        subcategory = pos_with_categories[2] if num_categories >= 2 else "*"
        subsubcategory = pos_with_categories[3] if num_categories >= 3 else "*"

        return Morpheme(
            "ja",
            token.text,
            pos,
            category,
            subcategory,
            subsubcategory,
            token.pos_,
            token.shape_,
            token.is_stop,
        )
