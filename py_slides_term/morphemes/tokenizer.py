import re
from typing import List, Any
import ja_core_news_sm
import en_core_web_sm

from .data import BaseMorpheme, MorphemeSpaCyDic
from py_slides_term.share.consts import HIRAGANA_REGEX, KATAKANA_REGEX, KANJI_REGEX


JAPANESE_REGEX = rf"({HIRAGANA_REGEX}|{KATAKANA_REGEX}|{KANJI_REGEX})"


class SpaCyTokenizer:
    # public
    def __init__(self):
        # pyright:reportUnknownMemberType=false
        self._ja_model = ja_core_news_sm.load()
        self._en_model = en_core_web_sm.load()

    def tokenize(self, text: str) -> List[BaseMorpheme]:
        if not text:
            return []

        japanese_regex = re.compile(rf"{JAPANESE_REGEX}")

        # pyright:reportUnknownArgumentType=false
        # pyright:reportUnknownLambdaType=false
        if japanese_regex.search(text):
            return list(
                map(
                    lambda token: self._create_japanese_morpheme(token),
                    self._ja_model(text),
                )
            )
        else:
            return list(
                map(
                    lambda token: self._create_english_morpheme(token),
                    self._en_model(text),
                )
            )

    def _create_japanese_morpheme(self, token: Any) -> MorphemeSpaCyDic:
        pos_with_categories = token.tag_.split("-")
        num_categories = len(pos_with_categories) - 1

        pos = pos_with_categories[0]
        category = pos_with_categories[1] if num_categories >= 1 else "*"
        subcategory = pos_with_categories[2] if num_categories >= 2 else "*"
        subsubcategory = pos_with_categories[3] if num_categories >= 3 else "*"

        return MorphemeSpaCyDic(
            token.text,
            pos,
            category,
            subcategory,
            subsubcategory,
            token.pos_,
            token.dep_,
            token.lemma_,
            token.shape_,
            token.is_stop,
        )

    def _create_english_morpheme(self, token: Any) -> MorphemeSpaCyDic:
        return MorphemeSpaCyDic(
            token.text,
            token.pos_,
            token.tag_,
            "*",
            "*",
            token.pos_,
            token.dep_,
            token.lemma_,
            token.shape_,
            token.is_stop,
        )
