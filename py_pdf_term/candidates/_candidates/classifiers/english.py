from py_pdf_term.tokenizers import Token

from .base import BaseTokenClassifier


class EnglishTokenClassifier(BaseTokenClassifier):
    """Token classifier for English tokens."""

    def inscope(self, token: Token) -> bool:
        return token.lang == "en"

    def is_symbol(self, token: Token) -> bool:
        return token.pos in {"SYM"}

    def is_connector_symbol(self, token: Token) -> bool:
        return token.surface_form == "-" and token.pos == "SYM"

    def is_connector_term(self, token: Token) -> bool:
        return token.pos == "ADP" and token.category == "IN"
