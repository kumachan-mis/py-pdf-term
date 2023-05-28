from py_pdf_term.tokenizers import Term, Token

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
    """Combiner of token filters and term filters.

    Args
    ----
        token_filters:
            List of token filters to filter tokens. If None, the default token filters
            are used. The default token filters are JapaneseTokenFilter and
            EnglishTokenFilter.

        term_filters:
            List of term filters to filter candidate terms. If None, the default term
            filters are used. The default term filters are JapaneseConcatenationFilter,
            EnglishConcatenationFilter, JapaneseSymbolLikeFilter,
            EnglishSymbolLikeFilter, JapaneseProperNounFilter,
            EnglishProperNounFilter, JapaneseNumericFilter, and EnglishNumericFilter.
    """

    def __init__(
        self,
        token_filters: list[BaseCandidateTokenFilter] | None = None,
        term_filters: list[BaseCandidateTermFilter] | None = None,
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

    def is_partof_candidate(self, tokens: list[Token], idx: int) -> bool:
        """Test if a token can be part of a candidate term using token filters.

        Args
        ----
            tokens:
                List of tokens.
            idx:
                Index of the token to be tested.

        Returns
        -------
            bool:
                True if the token can be part of a candidate term, False otherwise.
        """

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
        """Test if a term is a candidate term using term filters.

        Args
        ----
            term:
                Term to be tested.

        Returns
        -------
            bool:
                True if the term is a candidate term, False otherwise.
        """

        if all(map(lambda tf: not tf.inscope(term), self._term_filters)):
            return False

        return all(
            map(
                lambda tf: not tf.inscope(term) or tf.is_candidate(term),
                self._term_filters,
            )
        )
