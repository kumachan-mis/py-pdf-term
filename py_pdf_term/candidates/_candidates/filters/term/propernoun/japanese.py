from py_pdf_term._common.data import Term
from py_pdf_term.tokenizer import Token
from py_pdf_term.tokenizer.langs import JapaneseTokenClassifier

from ..base import BaseJapaneseCandidateTermFilter


class JapaneseProperNounFilter(BaseJapaneseCandidateTermFilter):
    def __init__(self) -> None:
        self._classifier = JapaneseTokenClassifier()

    def is_candidate(self, scoped_term: Term) -> bool:
        return not self._is_region_or_person(scoped_term)

    def _is_region_or_person(self, scoped_term: Term) -> bool:
        def is_region_or_person_token(token: Token) -> bool:
            return (
                (
                    token.pos == "名詞"
                    and token.category == "固有名詞"
                    and token.subcategory in {"人名", "地名"}
                )
                or self._classifier.is_modifying_particle(token)
                or self._classifier.is_connector_symbol(token)
            )

        return all(map(is_region_or_person_token, scoped_term.tokens))
