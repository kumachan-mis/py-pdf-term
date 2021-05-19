import re
from .base import BaseLanguageTokenizer
from typing import List, Any

import ja_core_news_sm

from ..data import Morpheme
from py_slides_term.share.consts import JAPANESE_REGEX, SYMBOL_REGEX


class JapaneseTokenizer(BaseLanguageTokenizer):
    # public
    def __init__(self):
        # pyright:reportUnknownMemberType=false
        self._ja_model = ja_core_news_sm.load()
        self._ja_model.disable_pipes("tok2vec", "parser", "ner", "attribute_ruler")

        self._ja_regex = re.compile(JAPANESE_REGEX)
        self._symbol_regex = re.compile(SYMBOL_REGEX)

    def inscope(self, text: str) -> bool:
        return self._ja_regex.search(text) is not None

    def tokenize(self, text: str) -> List[Morpheme]:
        # pyright:reportUnknownArgumentType=false
        # pyright:reportUnknownLambdaType=false
        return list(
            map(lambda token: self._create_morpheme(token), self._ja_model(text))
        )

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
