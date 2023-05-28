from py_pdf_term.tokenizers import Term

from .base import BaseTokenClassifier
from .english import EnglishTokenClassifier
from .japanese import JapaneseTokenClassifier


class MeaninglessMarker:
    """Marker class to mark meaningless tokens in a term.

    Args
    ----
        classifiers:
            List of token classifiers to mark meaningless tokens.
            If None, JapaneseTokenClassifier and EnglishTokenClassifier are used.
    """

    def __init__(self, classifiers: list[BaseTokenClassifier] | None = None) -> None:
        if classifiers is None:
            classifiers = [
                JapaneseTokenClassifier(),
                EnglishTokenClassifier(),
            ]

        self._classifiers = classifiers

    def mark(self, term: Term) -> Term:
        """Mark meaningless tokens in a term. The original term is modified in-place.

        Args
        ----
            term:
                Term to be marked.

        Returns
        -------
            Term:
                Term with meaningless tokens marked.
        """

        for token in term.tokens:
            token.is_meaningless = any(
                map(
                    lambda classifier: classifier.inscope(token)
                    and classifier.is_meaningless(token),
                    self._classifiers,
                )
            )
        return term
