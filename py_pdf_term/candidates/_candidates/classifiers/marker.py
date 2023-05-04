from typing import List, Optional

from py_pdf_term.tokenizers import Term

from .base import BaseTokenClassifier
from .english import EnglishTokenClassifier
from .japanese import JapaneseTokenClassifier


class MeaninglessMarker:
    """The marker class to mark meaningless tokens in a term.

    Args
    ----
        classifiers:
            A list of token classifiers to mark meaningless tokens.
            If None, JapaneseTokenClassifier and EnglishTokenClassifier are used.
    """

    def __init__(self, classifiers: Optional[List[BaseTokenClassifier]] = None) -> None:
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
                A term to be marked.

        Returns
        -------
            Term:
                A term with meaningless tokens marked.
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
