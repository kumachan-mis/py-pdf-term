from typing import List

from .base import BaseAugmenter
from ..filters import FilterCombiner
from py_slides_term.morphemes import JapaneseMorphemeClassifier
from py_slides_term.share.data import Term


class ModifyingParticleAugmenter(BaseAugmenter):
    # public
    def __init__(self, candidate_filter: FilterCombiner):
        self._filter = candidate_filter
        self._ja_classifier = JapaneseMorphemeClassifier()

    def augment(self, term: Term) -> List[Term]:
        num_morphemes = len(term.morphemes)
        modifying_particle_positions = (
            [-1]
            + [
                opsition
                for opsition in range(num_morphemes)
                if self._ja_classifier.is_modifying_particle(term.morphemes[opsition])
            ]
            + [num_morphemes]
        )
        num_positions = len(modifying_particle_positions)

        augmented_terms: List[Term] = []
        for length in range(1, num_positions - 1):
            for idx in range(num_positions - length):
                i = modifying_particle_positions[idx]
                j = modifying_particle_positions[idx + length]
                morphemes = term.morphemes[i + 1 : j]
                augmented_term = Term(morphemes, term.fontsize, True)
                if self._filter.is_candidate(augmented_term):
                    augmented_terms.append(augmented_term)

        return augmented_terms
