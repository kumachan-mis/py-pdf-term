from py_pdf_term.tokenizers import Term

from ..classifiers import BaseTokenClassifier
from .base import BaseSplitter


class RepeatSplitter(BaseSplitter):
    """Splitter to split a term by repeated tokens. For example, "quick sort merge
    sort heap sort" is split into "quick sort", "merge sort", and "heap sort".

    Args
    ----
        classifiers:
            List of token classifiers to classify tokens into specific categories.
            If None, the default classifiers are used. The default classifiers are
            JapaneseTokenClassifier and EnglishTokenClassifier.
    """

    def __init__(self, classifiers: list[BaseTokenClassifier] | None = None) -> None:
        super().__init__(classifiers=classifiers)

    def split(self, term: Term) -> list[Term]:
        if self._contains_connector_token(term):
            return [term]

        head, backward_splitted_terms = self._backward_split(term)
        forward_splitted_terms, center_term = self._forward_split(head)
        return forward_splitted_terms + [center_term] + backward_splitted_terms

    def _contains_connector_token(self, term: Term) -> bool:
        return any(
            map(
                lambda token: any(
                    map(
                        lambda classifier: classifier.is_connector(token),
                        self._classifiers,
                    )
                ),
                term.tokens,
            )
        )

    def _backward_split(self, term: Term) -> tuple[Term, list[Term]]:
        splitted_terms: list[Term] = []
        head = term.tokens
        fontsize, ncolor, augmented = term.fontsize, term.ncolor, term.augmented

        while True:
            head_length = len(head)
            j = head_length
            for i in range(head_length - 1, 0, -1):
                if str(head[i - 1]) != str(head[j - 1]):
                    continue
                splitted_term = Term(head[i:j], fontsize, ncolor, augmented)
                splitted_terms.append(splitted_term)
                head = head[:i]
                j = i

            if j == head_length:
                break

        splitted_terms.reverse()
        return Term(head, fontsize, ncolor, augmented), splitted_terms

    def _forward_split(self, term: Term) -> tuple[list[Term], Term]:
        splitted_terms: list[Term] = []
        tail = term.tokens
        fontsize, ncolor, augmented = term.fontsize, term.ncolor, term.augmented

        while True:
            tail_length = len(tail)
            i = 0
            for j in range(1, tail_length):
                if str(tail[0]) != str(tail[j - i]):
                    continue
                splitted_term = Term(tail[: j - i], fontsize, ncolor, augmented)
                splitted_terms.append(splitted_term)
                tail = tail[j - i :]
                i = j

            if i == 0:
                break

        return splitted_terms, Term(tail, fontsize, ncolor, augmented)
