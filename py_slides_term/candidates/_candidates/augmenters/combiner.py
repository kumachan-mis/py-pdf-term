from typing import List, Optional

from .base import BaseAugmenter
from .separation import JapaneseModifyingParticleAugmenter, EnglishAdpositionAugmenter
from py_slides_term._common.data import Term


class AugmenterCombiner:
    def __init__(self, augmenters: Optional[List[BaseAugmenter]] = None) -> None:
        if augmenters is None:
            augmenters = [
                JapaneseModifyingParticleAugmenter(),
                EnglishAdpositionAugmenter(),
            ]

        self._augmenters = augmenters

    def augment(self, term: Term) -> List[Term]:
        augmented_terms = [term]
        for augmenter in self._augmenters:
            start: List[Term] = []
            augmented_terms += sum(map(augmenter.augment, augmented_terms), start)

        return augmented_terms[1:]