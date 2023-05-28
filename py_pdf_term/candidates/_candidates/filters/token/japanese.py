import re

from py_pdf_term._common.consts import ENGLISH_REGEX, JAPANESE_REGEX, NUMBER_REGEX
from py_pdf_term.tokenizers import Token

from .base import BaseCandidateTokenFilter


class JapaneseTokenFilter(BaseCandidateTokenFilter):
    """Candidate token filter to filter out Japanese tokens which cannot be part of
    candidate terms.
    """

    def __init__(self) -> None:
        self._regex = re.compile(rf"({JAPANESE_REGEX}|{ENGLISH_REGEX}|{NUMBER_REGEX})+")

    def inscope(self, token: Token) -> bool:
        token_str = str(token)
        return token.lang == "ja" and (
            self._regex.fullmatch(token_str) is not None or token_str == "-"
        )

    def is_partof_candidate(self, tokens: list[Token], idx: int) -> bool:
        scoped_token = tokens[idx]
        num_tokens = len(tokens)

        match scoped_token.pos:
            case "名詞":
                return (
                    scoped_token.category in {"普通名詞"}
                    and scoped_token.subcategory
                    in {"一般", "サ変可能", "形状詞可能", "サ変形状詞可能", "助数詞可能"}
                ) or scoped_token.category in {"固有名詞", "数詞"}
            case "形状詞" | "形容詞":
                return (
                    scoped_token.category in {"一般"}
                    and idx < num_tokens - 1
                    and tokens[idx + 1].pos in {"名詞", "記号", "接尾辞", "形状詞", "形容詞"}
                )
            case "動詞":
                return (
                    scoped_token.category in {"一般"}
                    and idx < num_tokens - 1
                    and tokens[idx + 1].pos in {"接尾辞", "動詞"}
                )
            case "接頭辞":
                return (
                    idx < num_tokens - 1
                    and tokens[idx + 1].pos in {"名詞", "記号", "形状詞"}
                    # No line break
                )
            case "接尾辞":
                return (
                    scoped_token.category in {"名詞的", "形状詞的"}
                    and idx > 0
                    and tokens[idx - 1].pos in {"名詞", "形状詞", "動詞", "形容詞", "記号"}
                )
            case "助詞":
                return scoped_token.surface_form == "の"
            case "記号":
                return self._regex.match(str(scoped_token)) is not None
            case "補助記号":
                scoped_token_str = str(scoped_token)
                if scoped_token_str not in {"-", "・"}:
                    return False
                return (
                    0 < idx < num_tokens - 1
                    and self._regex.match(str(tokens[idx - 1])) is not None
                    and self._regex.match(str(tokens[idx + 1])) is not None
                )
            case _:
                return False
