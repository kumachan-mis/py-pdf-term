import re
from typing import List

from py_pdf_term._common.consts import ENGLISH_REGEX, NUMBER_REGEX
from py_pdf_term.tokenizer import Token

from .base import BaseCandidateTokenFilter


class EnglishTokenFilter(BaseCandidateTokenFilter):
    def __init__(self) -> None:
        self._regex = re.compile(rf"({ENGLISH_REGEX}|{NUMBER_REGEX})+")

    def inscope(self, token: Token) -> bool:
        token_str = str(token)
        return token.lang == "en" and (
            self._regex.fullmatch(token_str) is not None or token_str == "-"
        )

    def is_partof_candidate(self, tokens: List[Token], idx: int) -> bool:
        scoped_token = tokens[idx]
        num_tokens = len(tokens)

        if scoped_token.pos in {"NOUN", "PROPN", "NUM"}:
            return True
        elif scoped_token.pos == "ADJ":
            return (
                idx < num_tokens - 1
                and tokens[idx + 1].pos in {"NOUN", "PROPN", "ADJ", "VERB", "SYM"}
                # No line break
            )
        elif scoped_token.pos == "VERB":
            return scoped_token.category == "VBG" or (
                scoped_token.category == "VBN"
                and idx < num_tokens - 1
                and tokens[idx + 1].pos in {"NOUN", "PROPN", "ADJ", "VERB", "SYM"}
            )
        elif scoped_token.pos == "ADP":
            return scoped_token.category == "IN"
        elif scoped_token.pos == "SYM":
            return (
                scoped_token.surface_form == "-"
                and 0 < idx < num_tokens - 1
                and self._regex.match(str(tokens[idx - 1])) is not None
                and self._regex.match(str(tokens[idx + 1])) is not None
            )

        return False
