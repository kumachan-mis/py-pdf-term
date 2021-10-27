# pyright:reportUnknownMemberType=false
# pyright:reportUnknownArgumentType=false
# pyright:reportUnknownLambdaType=false

import re
from itertools import accumulate
from typing import Any, List

import ja_core_news_sm

from py_pdf_term._common.consts import JAPANESE_REGEX, NOSPACE_REGEX, SYMBOL_REGEX

from ..data import Token
from .base import BaseLanguageTokenizer

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

    def tokenize(self, text: str) -> List[Token]:
        text = SPACES.sub(" ", text).strip()
        orginal_space_pos = {
            match.start() - offset
            for offset, match in enumerate(re.finditer(r" ", text))
            if DELIM_SPASE.match(text, match.start()) is not None
        }

        text = DELIM_SPASE.sub("", text)
        tokens = list(map(self._create_token, self._model(text)))

        if not orginal_space_pos:
            return tokens

        tokenized_space_pos = set(
            accumulate(map(lambda token: len(str(token)), tokens))
        )
        if not orginal_space_pos.issubset(tokenized_space_pos):
            return tokens

        pos, i = 0, 0
        num_token = len(tokens) + len(orginal_space_pos)
        while i < num_token:
            if pos in orginal_space_pos:
                pos += len(str(tokens[i]))
                space = Token(
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
                tokens.insert(i, space)
                i += 2
            else:
                pos += len(str(tokens[i]))
                i += 1

        return tokens

    def _create_token(self, token: Any) -> Token:
        if self._symbol_regex.fullmatch(token.text):
            return Token(
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

        return Token(
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


class JapaneseTokenClassifier:
    def is_modifying_particle(self, token: Token) -> bool:
        return token.surface_form == "の" and token.pos == "助詞"

    def is_symbol(self, token: Token) -> bool:
        return token.pos in {"補助記号"}

    def is_connector_symbol(self, token: Token) -> bool:
        return token.surface_form in {"・", "-"} and token.pos == "補助記号"

    def is_meaningless(self, token: Token) -> bool:
        return self.is_symbol(token) or self.is_modifying_particle(token)
