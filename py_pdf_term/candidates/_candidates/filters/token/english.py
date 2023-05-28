import re

from py_pdf_term._common.consts import ENGLISH_REGEX, NUMBER_REGEX
from py_pdf_term.tokenizers import Token

from .base import BaseCandidateTokenFilter


class EnglishTokenFilter(BaseCandidateTokenFilter):
    """Candidate token filter to filter out English tokens which cannot be part of
    candidate terms.
    """

    def __init__(self) -> None:
        self._regex = re.compile(rf"({ENGLISH_REGEX}|{NUMBER_REGEX})+")

    def inscope(self, token: Token) -> bool:
        token_str = str(token)
        return token.lang == "en" and (
            self._regex.fullmatch(token_str) is not None or token_str == "-"
        )

    def is_partof_candidate(self, tokens: list[Token], idx: int) -> bool:
        scoped_token = tokens[idx]
        num_tokens = len(tokens)

        match scoped_token.pos:
            case "NOUN" | "PROPN" | "NUM":
                return True
            case "ADJ":
                return (
                    idx < num_tokens - 1
                    and tokens[idx + 1].pos in {"NOUN", "PROPN", "ADJ", "VERB", "SYM"}
                    # No line break
                )
            case "VERB":
                if scoped_token.category == "VBG":
                    return True
                elif scoped_token.category == "VBN":
                    return (
                        idx < num_tokens - 1
                        and tokens[idx + 1].pos
                        in {"NOUN", "PROPN", "ADJ", "VERB", "SYM"}
                        # No line break
                    )
                return False
            case "ADP":
                return scoped_token.category in {"IN"}
            case "SYM":
                return (
                    scoped_token.surface_form == "-"
                    and 0 < idx < num_tokens - 1
                    and self._regex.match(str(tokens[idx - 1])) is not None
                    and self._regex.match(str(tokens[idx + 1])) is not None
                )
            case _:
                return False
