import re
from typing import List, Any
import ja_core_news_sm
import en_core_web_sm

from .data import BaseMorpheme, SpaCyMorpheme
from py_slides_term.share.consts import JAPANESE_REGEX, ALPHABET_REGEX, SYMBOL_REGEX


class SpaCyTokenizer:
    # public
    def __init__(self):
        # pyright:reportUnknownMemberType=false
        self._ja_model = ja_core_news_sm.load()
        self._en_model = en_core_web_sm.load()
        self._ja_model.disable_pipes("tok2vec", "parser", "ner", "attribute_ruler")
        self._en_model.disable_pipes("parser", "ner", "lemmatizer")

        self._ja_regex = re.compile(JAPANESE_REGEX)
        self._en_regex = re.compile(ALPHABET_REGEX)
        self._symbol_regex = re.compile(SYMBOL_REGEX)

    def tokenize(self, text: str) -> List[BaseMorpheme]:
        if not text:
            return []

        # pyright:reportUnknownArgumentType=false
        # pyright:reportUnknownLambdaType=false
        if self._ja_regex.search(text):
            return list(
                map(
                    lambda token: self._create_japanese_morpheme(token),
                    self._ja_model(text),
                )
            )
        elif self._en_regex.search(text):
            return list(
                map(
                    lambda token: self._create_english_morpheme(token),
                    self._en_model(text),
                )
            )
        else:
            return []

    # private
    def _create_japanese_morpheme(self, token: Any) -> SpaCyMorpheme:
        if self._symbol_regex.fullmatch(token.text):
            return SpaCyMorpheme(
                "ja",
                token.text,
                "補助記号",
                "一般",
                "*",
                "*",
                "SYM",
                token.text,
                False,
            )

        pos_with_categories = token.tag_.split("-")
        num_categories = len(pos_with_categories) - 1

        pos = pos_with_categories[0]
        category = pos_with_categories[1] if num_categories >= 1 else "*"
        subcategory = pos_with_categories[2] if num_categories >= 2 else "*"
        subsubcategory = pos_with_categories[3] if num_categories >= 3 else "*"

        return SpaCyMorpheme(
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

    def _create_english_morpheme(self, token: Any) -> SpaCyMorpheme:
        if self._symbol_regex.fullmatch(token.text):
            return SpaCyMorpheme(
                "en",
                token.text,
                "SYM",
                "*",
                "*",
                "*",
                "SYM",
                token.text,
                False,
            )

        return SpaCyMorpheme(
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
