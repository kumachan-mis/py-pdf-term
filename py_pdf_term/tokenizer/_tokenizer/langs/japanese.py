# pyright:reportUnknownMemberType=false
# pyright:reportUnknownArgumentType=false
# pyright:reportUnknownLambdaType=false

import re
from itertools import accumulate
from typing import List, Any

import ja_core_news_sm

from .base import BaseLanguageTokenizer
from ..data import Morpheme
from py_pdf_term._common.consts import JAPANESE_REGEX, SYMBOL_REGEX, NOSPACE_REGEX

SPACES = re.compile(r"\s+")
DELIM_SPASE = re.compile(rf"(?<={NOSPACE_REGEX}) (?={NOSPACE_REGEX})")


class JapaneseTokenizer(BaseLanguageTokenizer):
    def __init__(self) -> None:
        enable_pipes = []
        self._model = ja_core_news_sm.load()
        self._model.select_pipes(enable=enable_pipes)

        self._ja_regex = re.compile(JAPANESE_REGEX)
        self._symbol_regex = re.compile(SYMBOL_REGEX)

    def inscope(self, text: str) -> bool:
        return self._ja_regex.search(text) is not None

    def tokenize(self, text: str) -> List[Morpheme]:
        text = SPACES.sub(" ", text).strip()
        orginal_space_pos = {
            match.start() - offset
            for offset, match in enumerate(re.finditer(r" ", text))
            if DELIM_SPASE.match(text, match.start()) is not None
        }

        text = DELIM_SPASE.sub("", text)
        morphemes = list(map(self._create_morpheme, self._model(text)))

        if not orginal_space_pos:
            return morphemes

        tokenized_space_pos = set(
            accumulate(map(lambda morpheme: len(str(morpheme)), morphemes))
        )
        if not orginal_space_pos.issubset(tokenized_space_pos):
            return morphemes

        pos, i = 0, 0
        num_morpheme = len(morphemes) + len(orginal_space_pos)
        while i < num_morpheme:
            if pos in orginal_space_pos:
                pos += len(str(morphemes[i]))
                space = Morpheme(
                    "ja",
                    " ",
                    "空白",
                    "*",
                    "*",
                    "*",
                    "SPACE",
                    " ",
                    " ",
                    False,
                )
                morphemes.insert(i, space)
                i += 2
            else:
                pos += len(str(morphemes[i]))
                i += 1

        return morphemes

    def _create_morpheme(self, token: Any) -> Morpheme:
        if self._symbol_regex.fullmatch(token.text):
            return Morpheme(
                "ja",
                token.text,
                "補助記号",
                "一般",
                "*",
                "*",
                "SYM",
                token.text,
                token.text,
                False,
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
            token.lemma_.lower(),
            token.shape_,
            token.is_stop,
        )
