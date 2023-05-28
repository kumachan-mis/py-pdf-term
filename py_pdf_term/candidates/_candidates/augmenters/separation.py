from abc import ABCMeta
from typing import Callable

from py_pdf_term.tokenizers import Term, Token

from ..classifiers import EnglishTokenClassifier, JapaneseTokenClassifier
from .base import BaseAugmenter


class BaseSeparationAugmenter(BaseAugmenter, metaclass=ABCMeta):
    """Base class for augmenters of a candidate term by separating tokens.

    Args
    ----
        is_separator:
            Function to test whether a token is a separator or not.
    """

    def __init__(self, is_separator: Callable[[Token], bool]) -> None:
        self._is_separator = is_separator

    def augment(self, term: Term) -> list[Term]:
        """Augment a candidate term by separating tokens.

        Args
        ----
            term:
                Candidate term to be augmented.

        Returns
        -------
            list[Term]:
                List of augmented terms. If a term consists of
                "A separator B separator C", the list contains the following terms:
                "A separator B separator C", "A separator B," "B separator C",
                "A", "B", "C".
        """

        num_tokens = len(term.tokens)
        separation_positions = (
            [-1]
            + [i for i in range(num_tokens) if self._is_separator(term.tokens[i])]
            + [num_tokens]
        )
        num_positions = len(separation_positions)

        augmented_terms: list[Term] = []
        for length in range(1, num_positions - 1):
            for idx in range(num_positions - length):
                i = separation_positions[idx]
                j = separation_positions[idx + length]
                tokens = term.tokens[i + 1 : j]
                augmented_term = Term(tokens, term.fontsize, term.ncolor, True)
                augmented_terms.append(augmented_term)

        return augmented_terms


class JapaneseConnectorTermAugmenter(BaseSeparationAugmenter):
    """An augmenter of a candidate term by separating tokens based on Japanese connector
    terms.
    """

    def __init__(self) -> None:
        classifier = JapaneseTokenClassifier()
        super().__init__(classifier.is_connector_term)

    def augment(self, term: Term) -> list[Term]:
        """Augment a candidate term by separating tokens based on Japanese connector
        terms.

        Args
        ----
            term:
                Candidate term to be augmented.

        Returns
        -------
            list[Term]:
                List of augmented terms.
                If a given term is not a Japanese term, the list is empty.
        """

        if term.lang != "ja":
            return []

        return super().augment(term)


class EnglishConnectorTermAugmenter(BaseSeparationAugmenter):
    """An augmenter of a candidate term by separating tokens based on English connector
    terms.
    """

    def __init__(self) -> None:
        classifier = EnglishTokenClassifier()
        super().__init__(classifier.is_connector_term)

    def augment(self, term: Term) -> list[Term]:
        """Augment a candidate term by separating tokens based on English connector
        terms.

        Args
        ----
            term:
                Candidate term to be augmented.

        Returns
        -------
            list[Term]:
                List of augmented terms.
                If a given term is not an English term, the list is empty.
        """

        if term.lang != "en":
            return []

        return super().augment(term)
