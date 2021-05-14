from abc import ABCMeta
from typing import List, Callable

from .base import BaseAugmenter
from ..filters import FilterCombiner
from py_slides_term.tokenizer import (
    BaseMorpheme,
    JapaneseMorphemeClassifier,
    EnglishMorphemeClassifier,
)
from py_slides_term.share.data import Term


class BaseSeparationAugmenter(BaseAugmenter, metaclass=ABCMeta):
    # public
    def __init__(
        self,
        candidate_filter: FilterCombiner,
        is_separator: Callable[[BaseMorpheme], bool] = lambda morpheme: False,
    ):
        self._filter = candidate_filter
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
                augmented_term = Term(morphemes, term.fontsize, True)
                if self._filter.is_candidate(augmented_term):
                    augmented_terms.append(augmented_term)

        return augmented_terms


class JapaneseModifyingParticleAugmenter(BaseSeparationAugmenter):
    # public
    def __init__(self, candidate_filter: FilterCombiner):
        classifier = JapaneseMorphemeClassifier()
        super().__init__(candidate_filter, classifier.is_modifying_particle)


class EnglishAdpositionAugmenter(BaseSeparationAugmenter):
    # public
    def __init__(self, candidate_filter: FilterCombiner):
        classifier = EnglishMorphemeClassifier()
        super().__init__(candidate_filter, classifier.is_adposition)
