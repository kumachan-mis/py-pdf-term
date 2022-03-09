from typing import List, Optional

from py_pdf_term._common.data import Term
from .base import BaseTokenClassifier
from .japanese import JapaneseTokenClassifier
from .english import EnglishTokenClassifier


class MeaninglessMarker:
    def __init__(self, classifiers: Optional[List[BaseTokenClassifier]] = None) -> None:
        if classifiers is None:
            classifiers = [
                JapaneseTokenClassifier(),
                EnglishTokenClassifier(),
            ]

        self._classifiers = classifiers

    def mark(self, term: Term) -> Term:
        for token in term.tokens:
            token.is_meaningless = any(
                map(
                    lambda classifier: classifier.inscope(token)
                    and classifier.is_meaningless(token),
                    self._classifiers,
                )
            )
        return term
