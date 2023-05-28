from py_pdf_term.tokenizers import Token

from .base import BaseTokenClassifier


class JapaneseTokenClassifier(BaseTokenClassifier):
    """Token classifier for Japanese tokens."""

    def inscope(self, token: Token) -> bool:
        return token.lang == "ja"

    def is_symbol(self, token: Token) -> bool:
        return token.pos in {"補助記号"}

    def is_connector_symbol(self, token: Token) -> bool:
        return token.surface_form in {"・", "-"} and token.pos == "補助記号"

    def is_connector_term(self, token: Token) -> bool:
        return token.surface_form == "の" and token.pos == "助詞"
