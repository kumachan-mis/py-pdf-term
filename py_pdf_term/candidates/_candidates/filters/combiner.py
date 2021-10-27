from typing import List, Optional

from py_pdf_term._common.data import Term
from py_pdf_term.tokenizer import Token

from .term import (
    BaseCandidateTermFilter,
    EnglishConcatenationFilter,
    EnglishNumericFilter,
    EnglishProperNounFilter,
    EnglishSymbolLikeFilter,
    JapaneseConcatenationFilter,
    JapaneseNumericFilter,
    JapaneseProperNounFilter,
    JapaneseSymbolLikeFilter,
)
from .token import BaseCandidateTokenFilter, EnglishTokenFilter, JapaneseTokenFilter


class FilterCombiner:
    def __init__(
        self,
        token_filters: Optional[List[BaseCandidateTokenFilter]] = None,
        term_filters: Optional[List[BaseCandidateTermFilter]] = None,
    ) -> None:
        if token_filters is None:
            token_filters = [
                JapaneseTokenFilter(),
                EnglishTokenFilter(),
            ]
        if term_filters is None:
            term_filters = [
                JapaneseConcatenationFilter(),
                EnglishConcatenationFilter(),
                JapaneseSymbolLikeFilter(),
                EnglishSymbolLikeFilter(),
                JapaneseProperNounFilter(),
                EnglishProperNounFilter(),
                JapaneseNumericFilter(),
                EnglishNumericFilter(),
            ]

        self._token_filters = token_filters
        self._term_filters = term_filters

    def is_partof_candidate(self, tokens: List[Token], idx: int) -> bool:
        token = tokens[idx]
        if all(map(lambda mf: not mf.inscope(token), self._token_filters)):
            return False

        return all(
            map(
                lambda mf: not mf.inscope(token) or mf.is_partof_candidate(tokens, idx),
                self._token_filters,
            )
        )

    def is_candidate(self, term: Term) -> bool:
        if all(map(lambda tf: not tf.inscope(term), self._term_filters)):
            return False

        return all(
            map(
                lambda tf: not tf.inscope(term) or tf.is_candidate(term),
                self._term_filters,
            )
        )
