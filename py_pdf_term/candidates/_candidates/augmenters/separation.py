from abc import ABCMeta
from typing import List, Callable

from .base import BaseAugmenter
from py_pdf_term.tokenizer import Morpheme
from py_pdf_term.tokenizer.langs import (
    JapaneseMorphemeClassifier,
    EnglishMorphemeClassifier,
)
from py_pdf_term._common.data import Term


class BaseSeparationAugmenter(BaseAugmenter, metaclass=ABCMeta):
    def __init__(self, is_separator: Callable[[Morpheme], bool]) -> None:
        self._is_separator = is_separator

    def augment(self, term: Term) -> List[Term]:
        num_morphemes = len(term.morphemes)
        separation_positions = (
            [-1]
            + [i for i in range(num_morphemes) if self._is_separator(term.morphemes[i])]
            + [num_morphemes]
        )
        num_positions = len(separation_positions)

        augmented_terms: List[Term] = []
        for length in range(1, num_positions - 1):
            for idx in range(num_positions - length):
                i = separation_positions[idx]
                j = separation_positions[idx + length]
                morphemes = term.morphemes[i + 1 : j]
                augmented_term = Term(morphemes, term.fontsize, term.ncolor, True)
                augmented_terms.append(augmented_term)

        return augmented_terms


class JapaneseModifyingParticleAugmenter(BaseSeparationAugmenter):
    def __init__(self) -> None:
        classifier = JapaneseMorphemeClassifier()
        super().__init__(classifier.is_modifying_particle)

    def augment(self, term: Term) -> List[Term]:
        if term.lang != "ja":
            return []

        return super().augment(term)


class EnglishAdpositionAugmenter(BaseSeparationAugmenter):
    def __init__(self) -> None:
        classifier = EnglishMorphemeClassifier()
        super().__init__(classifier.is_adposition)

    def augment(self, term: Term) -> List[Term]:
        if term.lang != "en":
            return []

        return super().augment(term)
