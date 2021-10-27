from typing import List, Tuple

from py_pdf_term._common.data import Term
from py_pdf_term.tokenizer.langs import EnglishTokenClassifier, JapaneseTokenClassifier

from .base import BaseSplitter


class RepeatSplitter(BaseSplitter):
    def __init__(self) -> None:
        self._ja_classifier = JapaneseTokenClassifier()
        self._en_classifier = EnglishTokenClassifier()

    def split(self, term: Term) -> List[Term]:
        if self._contains_connector_token(term):
            return [term]

        head, backward_splitted_terms = self._backward_split(term)
        forward_splitted_terms, center_term = self._forward_split(head)
        return forward_splitted_terms + [center_term] + backward_splitted_terms

    def _contains_connector_token(self, term: Term) -> bool:
        return any(
            map(
                lambda token: self._ja_classifier.is_modifying_particle(token)
                or self._ja_classifier.is_connector_symbol(token)
                or self._en_classifier.is_adposition(token)
                or self._en_classifier.is_connector_symbol(token),
                term.tokens,
            )
        )

    def _backward_split(self, term: Term) -> Tuple[Term, List[Term]]:
        splitted_terms: List[Term] = []
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

    def _forward_split(self, term: Term) -> Tuple[List[Term], Term]:
        splitted_terms: List[Term] = []
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
