from py_pdf_term.tokenizers import Term, Token

from ....classifiers import JapaneseTokenClassifier
from ..base import BaseJapaneseCandidateTermFilter


class JapaneseProperNounFilter(BaseJapaneseCandidateTermFilter):
    """Term filter to remove Japanese proper nouns from candidate terms."""

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
                or self._classifier.is_connector_term(token)
                or self._classifier.is_connector_symbol(token)
            )

        return all(map(is_region_or_person_token, scoped_term.tokens))
