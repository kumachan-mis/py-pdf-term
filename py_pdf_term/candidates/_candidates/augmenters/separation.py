from abc import ABCMeta
from typing import Callable, List

from py_pdf_term._common.data import Term
from py_pdf_term.tokenizer import Token
from py_pdf_term.tokenizer.langs import EnglishTokenClassifier, JapaneseTokenClassifier

from .base import BaseAugmenter


class BaseSeparationAugmenter(BaseAugmenter, metaclass=ABCMeta):
    def __init__(self, is_separator: Callable[[Token], bool]) -> None:
        self._is_separator = is_separator

    def augment(self, term: Term) -> List[Term]:
        num_tokens = len(term.tokens)
        separation_positions = (
            [-1]
            + [i for i in range(num_tokens) if self._is_separator(term.tokens[i])]
            + [num_tokens]
        )
        num_positions = len(separation_positions)

        augmented_terms: List[Term] = []
        for length in range(1, num_positions - 1):
            for idx in range(num_positions - length):
                i = separation_positions[idx]
                j = separation_positions[idx + length]
                tokens = term.tokens[i + 1 : j]
                augmented_term = Term(tokens, term.fontsize, term.ncolor, True)
                augmented_terms.append(augmented_term)

        return augmented_terms


class JapaneseModifyingParticleAugmenter(BaseSeparationAugmenter):
    def __init__(self) -> None:
        classifier = JapaneseTokenClassifier()
        super().__init__(classifier.is_modifying_particle)

    def augment(self, term: Term) -> List[Term]:
        if term.lang != "ja":
            return []

        return super().augment(term)


class EnglishAdpositionAugmenter(BaseSeparationAugmenter):
    def __init__(self) -> None:
        classifier = EnglishTokenClassifier()
        super().__init__(classifier.is_adposition)

    def augment(self, term: Term) -> List[Term]:
        if term.lang != "en":
            return []

        return super().augment(term)
