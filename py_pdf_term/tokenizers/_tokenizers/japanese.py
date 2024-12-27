import re
from itertools import accumulate
from typing import Any

import ja_core_news_sm

from py_pdf_term._common.consts import JAPANESE_REGEX, NOSPACE_REGEX, SYMBOL_REGEX

from .base import BaseLanguageTokenizer
from .data import Token

SPACES = re.compile(r"\s+")
DELIM_SPACE = re.compile(rf"(?<={NOSPACE_REGEX}) (?={NOSPACE_REGEX})")


class JapaneseTokenizer(BaseLanguageTokenizer):
    """Tokenizer for Japanese. This tokenizer uses SpaCy's ja_core_news_sm model."""

    def inscope(self, text: str) -> bool:
        return JapaneseTokenizer._regex.search(text) is not None

    def tokenize(self, scoped_text: str) -> list[Token]:
        scoped_text = SPACES.sub(" ", scoped_text).strip()
        orginal_space_pos = {
            regex_match.start() - offset
            for offset, regex_match in enumerate(re.finditer(r" ", scoped_text))
            if DELIM_SPACE.match(scoped_text, regex_match.start()) is not None
        }

        scoped_text = DELIM_SPACE.sub("", scoped_text)
        scoped_text = JapaneseTokenizer._symbol_regex.sub(r" \1 ", scoped_text)
        tokens = list(map(self._create_token, JapaneseTokenizer._model(scoped_text)))

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
                space = Token("ja", " ", "空白", "*", "*", " ")
                tokens.insert(i, space)
                i += 2
            else:
                pos += len(str(tokens[i]))
                i += 1

        return tokens

    def _create_token(self, token: Any) -> Token:
        if JapaneseTokenizer._symbol_regex.fullmatch(token.text):
            return Token("ja", token.text, "補助記号", "一般", "*", token.text)

        pos_with_categories = token.tag_.split("-")
        num_categories = len(pos_with_categories) - 1

        pos = pos_with_categories[0]
        category = pos_with_categories[1] if num_categories >= 1 else "*"
        subcategory = pos_with_categories[2] if num_categories >= 2 else "*"

        return Token("ja", token.text, pos, category, subcategory, token.lemma_.lower())

    @classmethod
    def class_init(cls) -> None:
        model = ja_core_news_sm.load()  # pyright: ignore[reportUnknownMemberType]
        enable_pipes: list[str] = []
        model.select_pipes(enable=enable_pipes)
        JapaneseTokenizer._model = model

        JapaneseTokenizer._regex = re.compile(JAPANESE_REGEX)
        JapaneseTokenizer._symbol_regex = re.compile(rf"({SYMBOL_REGEX})")


JapaneseTokenizer.class_init()
