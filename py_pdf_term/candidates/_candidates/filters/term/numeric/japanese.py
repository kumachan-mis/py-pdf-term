from py_pdf_term._common.data import Term
from py_pdf_term.tokenizer import Token
from py_pdf_term.tokenizer.langs import JapaneseTokenClassifier

from ..base import BaseJapaneseCandidateTermFilter


class JapaneseNumericFilter(BaseJapaneseCandidateTermFilter):
    def __init__(self) -> None:
        self._classifier = JapaneseTokenClassifier()

    def is_candidate(self, scoped_term: Term) -> bool:
        return not self._is_numeric_phrase(scoped_term)

    def _is_numeric_phrase(self, scoped_term: Term) -> bool:
        def is_numeric_or_meaningless(token: Token) -> bool:
            return (
                token.pos == "接頭辞"
                or (token.pos == "名詞" and token.category == "数詞")
                or (
                    token.pos == "名詞"
                    and token.category == "普通名詞"
                    and token.subcategory == "助数詞可能"
                )
                or token.pos == "接尾辞"
                or self._classifier.is_meaningless(token)
            )

        return all(map(is_numeric_or_meaningless, scoped_term.tokens))
