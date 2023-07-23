from abc import ABCMeta, abstractmethod

from py_pdf_term.tokenizers import Term

from ..classifiers import (
    BaseTokenClassifier,
    EnglishTokenClassifier,
    JapaneseTokenClassifier,
)


class BaseSplitter(metaclass=ABCMeta):
    """Base class for splitters of a wrongly concatenated term.

    Since text extraction from PDF is not perfect especially in a table or a figure,
    a term may be wrongly concatenated. For example, when a PDF file contains a table
    which shows the difference between quick sort, merge sort, and heap sort, the
    extracted text may be something like "quick sort merge sort heap sort". In this
    case, "quick sort", "merge sort", and "heap sort" are wrongly concatenated.

    This class is used to split a wrongly concatenated term into subterms.

    Args
    ----
        classifiers:
            List of token classifiers to classify tokens into specific categories.
            If None, the default classifiers are used. The default classifiers are
            JapaneseTokenClassifier and EnglishTokenClassifier.
    """

    def __init__(self, classifiers: list[BaseTokenClassifier] | None = None) -> None:
        if classifiers is None:
            classifiers = [
                JapaneseTokenClassifier(),
                EnglishTokenClassifier(),
            ]

        self._classifiers = classifiers

    @abstractmethod
    def split(self, term: Term) -> list[Term]:
        """Split a wrongly concatenated term.

        Args
        ----
            term:
                Wrongly concatenated term to be split.

        Returns
        -------
            list[Term]:
                List of split terms.
        """
        raise NotImplementedError(f"{self.__class__.__name__}.split()")
